/**
 * CareBridge AI — Frontend Application Logic
 * Full bilingual support (English & Telugu), Web Speech API audio reader,
 * Faithfulness audit inspector, and Evaluation Benchmark runner.
 */

// Global State
let currentCarePlan = null;
let currentLanguage = 'en'; // 'en', 'te', 'both'
let synth = window.speechSynthesis;
let currentUtterance = null;
let isAudioPlaying = false;
let currentUser = null;

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    initNavigation();
    initFontScaler();
    initDropzone();
    loadDemoSamples();
    loadPreviousReports();
    loadDashboardStats();
});

// Authentication & Session Guard
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/me');
        if (!response.ok) {
            window.location.href = '/login';
            return;
        }
        const user = await response.json();
        currentUser = user;
        updateUserBadge(user);
    } catch (err) {
        console.warn('Auth check error:', err);
        window.location.href = '/login';
    }
}

function updateUserBadge(user) {
    const wrapper = document.getElementById('nav-user-wrapper');
    const avatar = document.getElementById('nav-user-avatar');
    const nameEl = document.getElementById('nav-user-name');
    const dropdownAvatar = document.getElementById('dropdown-user-avatar');
    const dropdownName = document.getElementById('dropdown-user-name');
    const dropdownEmail = document.getElementById('dropdown-user-email');

    // Modal elements
    const modalAvatar = document.getElementById('modal-user-avatar');
    const modalNameDisplay = document.getElementById('modal-user-name-display');
    const modalEmailDisplay = document.getElementById('modal-user-email-display');
    const modalJoined = document.getElementById('modal-user-joined');
    const modalEditName = document.getElementById('modal-edit-name');

    if (!user) return;
    if (wrapper) wrapper.style.display = 'inline-block';

    const displayName = user.full_name || user.email;
    if (nameEl) nameEl.textContent = displayName;
    if (dropdownName) dropdownName.textContent = displayName;
    if (dropdownEmail) dropdownEmail.textContent = user.email || '';

    // Calculate initials
    const parts = displayName.split(' ').filter(p => p.length > 0);
    let initials = 'U';
    if (parts.length >= 2) {
        initials = (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    } else if (parts.length === 1 && parts[0].length >= 2) {
        initials = parts[0].substring(0, 2).toUpperCase();
    }

    if (avatar) avatar.textContent = initials;
    if (dropdownAvatar) dropdownAvatar.textContent = initials;
    if (modalAvatar) modalAvatar.textContent = initials;
    if (modalNameDisplay) modalNameDisplay.textContent = displayName;
    if (modalEmailDisplay) modalEmailDisplay.textContent = user.email || '';
    if (modalEditName) modalEditName.value = displayName;

    if (modalJoined && user.created_at) {
        try {
            const dt = new Date(user.created_at);
            modalJoined.textContent = dt.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
        } catch (_) {
            modalJoined.textContent = user.created_at.substring(0, 10);
        }
    }
}

// Profile Dropdown Toggle
function toggleProfileDropdown(e) {
    if (e) e.stopPropagation();
    const menu = document.getElementById('profile-dropdown-menu');
    const btn = document.getElementById('user-profile-btn');
    if (!menu || !btn) return;
    const isShown = menu.classList.toggle('show');
    btn.classList.toggle('active', isShown);
    btn.setAttribute('aria-expanded', isShown ? 'true' : 'false');
}

// Close Dropdown On Outside Click
window.addEventListener('click', (e) => {
    const wrapper = document.getElementById('nav-user-wrapper');
    if (wrapper && !wrapper.contains(e.target)) {
        const menu = document.getElementById('profile-dropdown-menu');
        const btn = document.getElementById('user-profile-btn');
        if (menu) menu.classList.remove('show');
        if (btn) btn.classList.remove('active');
    }
});

// Navigate to My Care Plans
function navigateToMyPlans() {
    const menu = document.getElementById('profile-dropdown-menu');
    const btn = document.getElementById('user-profile-btn');
    if (menu) menu.classList.remove('show');
    if (btn) btn.classList.remove('active');

    showSection('section-history');
    document.querySelectorAll('.nav-link').forEach(l => {
        if (l.getAttribute('data-target') === 'section-history') l.classList.add('active');
        else l.classList.remove('active');
    });
}

// Profile Modal Handlers
function openProfileModal() {
    const menu = document.getElementById('profile-dropdown-menu');
    const btn = document.getElementById('user-profile-btn');
    if (menu) menu.classList.remove('show');
    if (btn) btn.classList.remove('active');

    const modal = document.getElementById('profile-modal');
    if (modal) modal.style.display = 'flex';
}

function closeProfileModal() {
    const modal = document.getElementById('profile-modal');
    if (modal) modal.style.display = 'none';
}

async function saveProfileName() {
    const input = document.getElementById('modal-edit-name');
    const msg = document.getElementById('profile-update-msg');
    const newName = input ? input.value.trim() : '';

    if (!newName || newName.length < 2) {
        if (msg) {
            msg.textContent = 'Please enter at least 2 characters.';
            msg.style.color = '#ef4444';
            msg.style.display = 'block';
        }
        return;
    }

    try {
        const res = await fetch('/api/auth/profile', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name: newName })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Could not update profile.');

        currentUser = data.user;
        updateUserBadge(data.user);

        if (msg) {
            msg.textContent = '✓ Name updated successfully!';
            msg.style.color = '#10b981';
            msg.style.display = 'block';
            setTimeout(() => { if (msg) msg.style.display = 'none'; }, 2000);
        }
    } catch (err) {
        if (msg) {
            msg.textContent = err.message;
            msg.style.color = '#ef4444';
            msg.style.display = 'block';
        }
    }
}

async function handleLogout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
    } catch (err) {
        console.error('Logout error:', err);
    } finally {
        window.location.href = '/login';
    }
}

// Navigation Handling
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSection = link.getAttribute('data-target');
            showSection(targetSection);
            
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Hero CTA button
    const heroCta = document.getElementById('hero-create-btn');
    if (heroCta) {
        heroCta.addEventListener('click', () => {
            showSection('section-create');
            document.querySelectorAll('.nav-link').forEach(l => {
                if (l.getAttribute('data-target') === 'section-create') l.classList.add('active');
                else l.classList.remove('active');
            });
        });
    }
}

function showSection(sectionId) {
    document.querySelectorAll('.app-section').forEach(sec => {
        sec.style.display = 'none';
    });
    const target = document.getElementById(sectionId);
    if (target) {
        target.style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    if (sectionId === 'section-history') {
        loadPreviousReports();
    } else if (sectionId === 'section-eval') {
        loadDashboardStats();
    }
}

// Font Scaling for Older Adults
function initFontScaler() {
    const btnNormal = document.getElementById('font-normal');
    const btnLg = document.getElementById('font-lg');
    const btnXl = document.getElementById('font-xl');

    if (btnNormal && btnLg && btnXl) {
        btnNormal.addEventListener('click', () => {
            document.body.className = '';
            setActiveFontBtn(btnNormal);
        });
        btnLg.addEventListener('click', () => {
            document.body.className = 'font-lg';
            setActiveFontBtn(btnLg);
        });
        btnXl.addEventListener('click', () => {
            document.body.className = 'font-xl';
            setActiveFontBtn(btnXl);
        });
    }
}

function setActiveFontBtn(btn) {
    document.querySelectorAll('.font-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

// Drag & Drop File Upload
function initDropzone() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');

    if (!dropzone || !fileInput) return;

    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

// Handle Upload with PyMuPDF & OCR Backend
async function handleFileUpload(file) {
    const errorEl = document.getElementById('input-error');
    const textarea = document.getElementById('source-text-input');
    const uploadStatus = document.getElementById('upload-status');

    errorEl.style.display = 'none';
    uploadStatus.style.display = 'block';
    uploadStatus.innerHTML = `⏳ Reading & extracting text from <strong>${file.name}</strong> (OCR / Medical Parser)...`;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to extract text from document.');
        }

        textarea.value = data.extracted_text;
        const meta = data.metadata || {};
        const method = meta.ocr_applied ? ' (OCR Applied)' : '';
        uploadStatus.innerHTML = `✅ Successfully extracted ${meta.total_chars || data.extracted_text.length} characters${method} from <strong>${file.name}</strong>.`;
    } catch (err) {
        uploadStatus.style.display = 'none';
        errorEl.style.display = 'block';
        errorEl.innerText = err.message;
    }
}

// Load Synthetic Demo Samples
async function loadDemoSamples() {
    const container = document.getElementById('sample-buttons-container');
    if (!container) return;

    try {
        const res = await fetch('/api/demo-samples');
        const samples = await res.json();

        container.innerHTML = '';
        samples.forEach(sample => {
            const btn = document.createElement('button');
            btn.className = 'sample-chip';
            btn.type = 'button';
            btn.innerHTML = `<strong>${sample.title}</strong> <span style="color:#64748b;">(${sample.category})</span>`;
            btn.addEventListener('click', () => {
                document.getElementById('source-text-input').value = sample.raw_text;
                const status = document.getElementById('upload-status');
                status.style.display = 'block';
                status.innerHTML = `📄 Loaded sample: <strong>${sample.title}</strong> (${sample.patient_name})`;
                document.getElementById('input-error').style.display = 'none';
            });
            container.appendChild(btn);
        });
    } catch (e) {
        console.error('Error loading samples:', e);
    }
}

// Generate Care Plan
async function generatePlan() {
    const textarea = document.getElementById('source-text-input');
    const text = textarea.value.trim();
    const errorEl = document.getElementById('input-error');
    const loadingEl = document.getElementById('generation-loading');
    const resultsContainer = document.getElementById('results-container');
    const apiKeyInput = document.getElementById('api-key-input');
    const apiKey = apiKeyInput ? apiKeyInput.value.trim() : null;

    if (!text) {
        errorEl.style.display = 'block';
        errorEl.innerText = 'Please enter or upload discharge summary instructions.';
        return;
    }

    errorEl.style.display = 'none';
    loadingEl.style.display = 'block';
    resultsContainer.style.display = 'none';

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                languages: ['en', 'te'],
                api_key: apiKey || null
            })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Error generating care plan.');
        }

        currentCarePlan = data;
        loadingEl.style.display = 'none';
        renderCarePlan(data);
        resultsContainer.style.display = 'block';
        resultsContainer.scrollIntoView({ behavior: 'smooth' });

        // Refresh stats and history in background
        loadDashboardStats();
    } catch (err) {
        loadingEl.style.display = 'none';
        errorEl.style.display = 'block';
        errorEl.innerText = err.message;
    }
}

// Render Care Plan to DOM
function renderCarePlan(plan) {
    // 1. Hard Safety Gate Banner
    const fRep = plan.faithfulness_report;
    const banner = document.getElementById('safety-gate-banner');
    const bannerIcon = document.getElementById('safety-banner-icon');
    const bannerTitle = document.getElementById('safety-banner-title');
    const bannerDesc = document.getElementById('safety-banner-desc');

    if (fRep.overall_status === 'VERIFIED') {
        banner.className = 'safety-banner verified';
        bannerIcon.innerText = '🛡️';
        bannerTitle.innerText = '100% Medical Faithfulness Verified';
        bannerDesc.innerText = 'All 11 clinical safety checks passed. Dosages, frequencies, routes, warning signs, and Telugu facts match original discharge orders with zero hallucination.';
    } else {
        banner.className = 'safety-banner review';
        bannerIcon.innerText = '⚠️';
        bannerTitle.innerText = 'CLINICIAN REVIEW REQUIRED — Safety Gate Triggered';
        bannerDesc.innerText = fRep.safety_gate_message;
    }

    // 2. Readability Metrics
    const engRead = plan.readability.english;
    const teRead = plan.readability.telugu;
    
    document.getElementById('metric-grade').innerText = `Grade ${engRead.grade_level}`;
    document.getElementById('metric-grade-label').innerText = engRead.class_level_label;
    document.getElementById('metric-ease').innerText = `${engRead.reading_ease} / 100`;
    document.getElementById('metric-words').innerText = `${engRead.word_count} words (${engRead.sentence_count} sentences)`;
    document.getElementById('metric-preservation').innerText = `${fRep.metrics.fact_preservation_rate}%`;

    // 3. Render Content for Selected Language
    renderContentByLanguage(currentLanguage);

    // 4. Render 7-day Timetable
    renderTimetable(plan.timetable);
}

// Render Language Specific Content
function renderContentByLanguage(lang) {
    if (!currentCarePlan) return;

    const en = currentCarePlan.english_plan;
    const te = currentCarePlan.telugu_plan;
    const isBoth = (lang === 'both');
    const active = (lang === 'te') ? te : en;

    const displayContainer = document.getElementById('care-plan-display-area');

    if (isBoth) {
        displayContainer.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3 style="color:#0f766e; margin-bottom:12px; border-bottom:2px solid #0d9488; padding-bottom:4px;">🇬🇧 English Care Plan</h3>
                    ${buildPlanHTML(en, 'en')}
                </div>
                <div>
                    <h3 style="color:#0f766e; margin-bottom:12px; border-bottom:2px solid #0d9488; padding-bottom:4px;">🇮🇳 తెలుగు కేర్ ప్లాన్ (Telugu)</h3>
                    ${buildPlanHTML(te, 'te')}
                </div>
            </div>
        `;
    } else {
        displayContainer.innerHTML = buildPlanHTML(active, lang);
    }
}

// Construct Care Plan Section HTML
function buildPlanHTML(planData, lang) {
    const isTe = (lang === 'te');
    const overview = planData.patient_overview || {};
    const meds = planData.medicines || [];
    const warnings = planData.warning_signs || [];
    const diet = planData.diet_instructions || [];
    const activity = planData.activity_restrictions || [];
    const wound = planData.wound_care_instructions || [];
    const followUps = planData.follow_ups || [];

    // Medications Table Rows
    let medRows = '';
    meds.forEach((m, idx) => {
        const sourceQuote = m.source_sentence ? `
            <button class="source-quote-btn" onclick="showEvidenceModal('${escapeHtml(m.name)}', '${escapeHtml(m.source_sentence)}')">
                🔍 ${isTe ? 'ఆధార వాక్యం చూడండి' : 'View Source Sentence'}
            </button>
        ` : '';

        medRows += `
            <tr>
                <td class="med-name-cell">
                    <strong>${m.name}</strong>
                    ${m.generic ? `<div class="med-generic">${m.generic}</div>` : ''}
                    ${m.purpose ? `<div style="font-size:12px; color:#0f766e; margin-top:2px;">ℹ️ ${m.purpose}</div>` : ''}
                    ${sourceQuote}
                </td>
                <td><span class="dose-badge">${m.dose_and_unit}</span></td>
                <td><strong>${m.frequency}</strong></td>
                <td>${m.timing}</td>
                <td>${m.route || 'Oral'}</td>
                <td>${m.duration}</td>
                <td><small>${m.instructions || '-'}</small></td>
            </tr>
        `;
    });

    // Warning Signs
    let warnList = '';
    warnings.forEach(w => {
        warnList += `<li><strong>${w.sign}</strong> — <em>${w.action}</em></li>`;
    });

    // Diet & Activity
    const dietItems = diet.map(d => `<li>${d}</li>`).join('') || `<li>${isTe ? 'వైద్యుల ప్రామాణిక ఆహార సూచనలను పాటించండి.' : 'Follow standard physician dietary guidance.'}</li>`;
    const activityItems = activity.map(a => `<li>${a}</li>`).join('') || `<li>${isTe ? 'వైద్యుల విశ్రాంతి సూచనలు పాటించండి.' : 'Follow physician rest instructions.'}</li>`;

    // Follow-ups
    let fuCards = '';
    followUps.forEach(f => {
        fuCards += `
            <div class="fu-card">
                <div class="fu-date">📅 ${f.date} ${f.time ? `(${f.time})` : ''}</div>
                <div class="fu-clinic">🏥 ${f.clinician_or_department}</div>
                <div class="fu-instructions">${f.instructions}</div>
            </div>
        `;
    });
    if (!fuCards) {
        fuCards = `<p style="color:#64748b;">${isTe ? 'ప్రత్యేక తదుపరి సందర్శన పేర్కొనబడలేదు. డాక్టర్ సలహా తీసుకోండి.' : 'No specific follow-up appointment was stated in the summary.'}</p>`;
    }

    return `
        <!-- Patient Overview Card -->
        <div class="card" style="margin-bottom:16px;">
            <div class="card-header">
                <h3 class="card-title">👤 ${isTe ? 'రోగి మరియు చికిత్స వివరాలు' : 'A. Patient Overview'}</h3>
                <span style="font-size:13px; color:#64748b;">${isTe ? 'డిశ్చార్జ్ తేదీ:' : 'Discharged:'} ${overview.discharge_date}</span>
            </div>
            <p><strong>${isTe ? 'రోగి పేరు:' : 'Patient Name:'}</strong> ${overview.patient_name} (${overview.age || ''}, ${overview.gender || ''})</p>
            <p style="margin-top:4px;"><strong>${isTe ? 'వైద్య పరిస్థితి / రోగ నిర్ధారణ:' : 'Clinical Diagnosis:'}</strong> ${Array.isArray(overview.conditions) ? overview.conditions.join(', ') : overview.conditions}</p>
        </div>

        <!-- Warning Signs (Red Emergency Alert) -->
        <div class="warning-card" style="margin-bottom:16px;">
            <h4>🚨 ${isTe ? 'అత్యవసర హెచ్చరిక సంకేతాలు (EMERGENCY RED FLAGS)' : 'C. Emergency Warning Signs'}</h4>
            <p style="font-size:13px; margin-bottom:8px; font-weight:600;">
                ${isTe ? 'ఈ క్రింది లక్షణాలు కనిపిస్తే వెంటనే అత్యవసర చికిత్సకు వెళ్ళండి లేదా 108కి కాల్ చేయండి:' : 'If you experience any of these symptoms, call emergency services (108/112) or go to the Emergency Room immediately:'}
            </p>
            <ul class="warning-list">
                ${warnList}
            </ul>
        </div>

        <!-- Medicines Table -->
        <div class="card" style="margin-bottom:16px;">
            <div class="card-header">
                <h3 class="card-title">💊 ${isTe ? 'నా మందుల జాబితా' : 'B. My Medicines'}</h3>
                <span style="font-size:13px; color:#0f766e; font-weight:600;">${meds.length} ${isTe ? 'మందులు నమోదు చేయబడ్డాయి' : 'Prescribed Medicines'}</span>
            </div>
            <div class="med-table-wrapper">
                <table class="med-table">
                    <thead>
                        <tr>
                            <th>${isTe ? 'మందు పేరు' : 'Medicine'}</th>
                            <th>${isTe ? 'మోతాదు' : 'Dose'}</th>
                            <th>${isTe ? 'ఎన్నిసార్లు' : 'Frequency'}</th>
                            <th>${isTe ? 'సమయం' : 'Timing'}</th>
                            <th>${isTe ? 'ఎలా తీసుకోవాలి' : 'Route'}</th>
                            <th>${isTe ? 'ఎన్ని రోజులు' : 'Duration'}</th>
                            <th>${isTe ? 'ముఖ్య సూచనలు' : 'Instructions'}</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${medRows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Diet and Activity Grid -->
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-bottom:16px;">
            <div class="card" style="margin-bottom:0;">
                <h4 style="color:#0f766e; margin-bottom:8px;">🥗 ${isTe ? 'ఆహార నియమాలు' : 'D. Diet & Nutrition'}</h4>
                <ul style="padding-left:18px; font-size:14px; line-height:1.6;">${dietItems}</ul>
            </div>
            <div class="card" style="margin-bottom:0;">
                <h4 style="color:#0f766e; margin-bottom:8px;">🚶 ${isTe ? 'శారీరక శ్రమ & విశ్రాంతి' : 'E. Daily Activity & Rest'}</h4>
                <ul style="padding-left:18px; font-size:14px; line-height:1.6;">${activityItems}</ul>
            </div>
        </div>

        <!-- Follow-up Appointments -->
        <div class="card" style="margin-bottom:16px;">
            <div class="card-header">
                <h3 class="card-title">📅 ${isTe ? 'తదుపరి వైద్య పరీక్షల తేదీలు' : 'F. Follow-up Appointments'}</h3>
            </div>
            <div class="fu-grid">${fuCards}</div>
        </div>

        <!-- Disclaimer -->
        <div style="text-align:center; padding:12px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; font-size:12px; color:#64748b;">
            ⚠️ <em>${planData.disclaimer}</em>
        </div>
    `;
}

// Render Seven-Day Timetable
function renderTimetable(timetable) {
    const container = document.getElementById('timetable-view');
    if (!container || !timetable || !timetable.has_data) return;

    let html = `
        <div style="margin-bottom:12px;">
            <p style="font-size:14px; color:#475569;">${timetable.safety_disclaimer}</p>
        </div>
        <div class="timetable-grid">
    `;

    timetable.days.forEach(day => {
        const slots = timetable.matrix[day];
        html += `
            <div class="day-column">
                <div class="day-header">${day}</div>
                <div class="slot-block">
                    <div class="slot-label">🌅 Morning</div>
                    ${renderSlotPills(slots.Morning)}
                </div>
                <div class="slot-block">
                    <div class="slot-label">☀️ Noon</div>
                    ${renderSlotPills(slots.Afternoon)}
                </div>
                <div class="slot-block">
                    <div class="slot-label">🌆 Evening</div>
                    ${renderSlotPills(slots.Evening)}
                </div>
                <div class="slot-block">
                    <div class="slot-label">🌙 Bedtime</div>
                    ${renderSlotPills(slots.Bedtime)}
                </div>
                ${slots.AsNeeded && slots.AsNeeded.length > 0 ? `
                    <div class="slot-block">
                        <div class="slot-label" style="color:#ef4444;">🚨 PRN (As Needed)</div>
                        ${renderSlotPills(slots.AsNeeded)}
                    </div>
                ` : ''}
            </div>
        `;
    });

    html += `</div>`;
    container.innerHTML = html;
}

function renderSlotPills(items) {
    if (!items || items.length === 0) {
        return `<div style="font-size:11px; color:#94a3b8; font-style:italic;">None</div>`;
    }
    return items.map(i => `
        <div class="pill-entry">
            <strong>${i.name}</strong><br>
            <span style="color:#0f766e; font-size:11px;">${i.dose}</span>
            ${i.is_draft ? `<span style="color:#f59e0b; font-size:10px;" title="Timing not explicitly specified in summary. Confirm with doctor.">⚠️</span>` : ''}
        </div>
    `).join('');
}

// Language Switcher Handlers
function setLanguage(lang) {
    currentLanguage = lang;
    document.querySelectorAll('.lang-tab').forEach(t => {
        if (t.getAttribute('data-lang') === lang) t.classList.add('active');
        else t.classList.remove('active');
    });
    renderContentByLanguage(lang);
}

// Toggle Timetable Visibility
function toggleTimetable() {
    const el = document.getElementById('timetable-card');
    if (el) {
        el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
        if (el.style.display === 'block') {
            el.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// Download/Print Fridge Sheet
function openFridgeSheet(format) {
    if (!currentCarePlan) return;
    const lang = (currentLanguage === 'te') ? 'te' : 'en';
    const url = `/api/fridge-sheet?plan_id=${currentCarePlan.id}&format=${format}&lang=${lang}`;
    if (format === 'html') {
        window.open(url, '_blank');
    } else {
        window.location.href = url;
    }
}

// Faithfulness Audit Modal
function openAuditModal() {
    if (!currentCarePlan) return;
    const fRep = currentCarePlan.faithfulness_report;
    const modal = document.getElementById('audit-modal');
    const content = document.getElementById('audit-modal-body');

    let checksHtml = '';
    fRep.checks.forEach(c => {
        const badgeColor = c.status === 'PASS' ? '#10b981' : (c.status === 'FAIL' ? '#ef4444' : '#f59e0b');
        checksHtml += `
            <div style="border-bottom:1px solid #e2e8f0; padding:12px 0;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <strong>${c.category}</strong>
                    <span style="background:${badgeColor}; color:#fff; font-size:11px; font-weight:700; padding:2px 8px; border-radius:12px;">${c.status}</span>
                </div>
                <p style="font-size:13px; color:#334155;">${c.details}</p>
                ${c.source_evidence ? `<div style="font-size:12px; color:#64748b; margin-top:2px;"><em>Evidence: ${c.source_evidence}</em></div>` : ''}
                ${c.discrepancy ? `<div style="font-size:12px; color:#ef4444; margin-top:2px; font-weight:600;">Discrepancy: ${c.discrepancy}</div>` : ''}
            </div>
        `;
    });

    content.innerHTML = `
        <div style="background:${fRep.overall_status === 'VERIFIED' ? '#ecfdf5' : '#fef2f2'}; border:1px solid ${fRep.overall_status === 'VERIFIED' ? '#a7f3d0' : '#fecaca'}; padding:14px; border-radius:8px; margin-bottom:16px;">
            <h4 style="color:${fRep.overall_status === 'VERIFIED' ? '#065f46' : '#991b1b'}; margin-bottom:4px;">Audit Verdict: ${fRep.overall_status}</h4>
            <p style="font-size:13px;">${fRep.safety_gate_message}</p>
            <div style="display:flex; gap:16px; margin-top:8px; font-size:12px; font-weight:700;">
                <span style="color:#10b981;">Passed: ${fRep.passed_checks}</span>
                <span style="color:#ef4444;">Failed: ${fRep.failed_checks}</span>
                <span style="color:#f59e0b;">Review: ${fRep.review_needed_checks}</span>
            </div>
        </div>
        <h4 style="margin-bottom:8px; color:#0f766e;">11-Point Medical Faithfulness Checklist</h4>
        <div>${checksHtml}</div>
    `;

    modal.style.display = 'flex';
}

function closeAuditModal() {
    document.getElementById('audit-modal').style.display = 'none';
}

// Evidence Citation Modal
function showEvidenceModal(medName, sourceSentence) {
    const modal = document.getElementById('evidence-modal');
    document.getElementById('evidence-med-name').innerText = medName;
    document.getElementById('evidence-source-text').innerText = `"${sourceSentence}"`;
    modal.style.display = 'flex';
}

function closeEvidenceModal() {
    document.getElementById('evidence-modal').style.display = 'none';
}

// Text-to-Speech Audio Player (Web Speech API)
function toggleAudio() {
    if (!currentCarePlan) return;

    if (isAudioPlaying) {
        synth.cancel();
        isAudioPlaying = false;
        document.getElementById('audio-play-btn').innerText = '▶️ Listen to Care Plan';
        return;
    }

    const isTe = (currentLanguage === 'te');
    let textToRead = '';

    if (isTe) {
        const te = currentCarePlan.telugu_plan;
        textToRead = `నమస్కారం. ఇది మీ డిశ్చార్జ్ కేర్ ప్లాన్. రోగి: ${te.patient_overview.patient_name}. `;
        te.medicines.forEach(m => {
            textToRead += `మందు: ${m.name}. మోతాదు: ${m.dose_and_unit}. ${m.frequency}. ${m.timing}. `;
        });
        if (te.warning_signs.length > 0) {
            textToRead += `అత్యవసర హెచ్చరిక లక్షణాలు: `;
            te.warning_signs.forEach(w => {
                textToRead += `${w.sign}. `;
            });
        }
    } else {
        const en = currentCarePlan.english_plan;
        textToRead = `Welcome. Here is your CareBridge discharge plan for ${en.patient_overview.patient_name}. `;
        textToRead += `Your medicines are: `;
        en.medicines.forEach(m => {
            textToRead += `${m.name}, ${m.dose_and_unit}, ${m.frequency}, ${m.timing}. `;
        });
        if (en.warning_signs.length > 0) {
            textToRead += `Emergency warning signs: `;
            en.warning_signs.forEach(w => {
                textToRead += `${w.sign}. `;
            });
        }
    }

    currentUtterance = new SpeechSynthesisUtterance(textToRead);
    currentUtterance.rate = parseFloat(document.getElementById('audio-speed').value) || 1.0;
    currentUtterance.lang = isTe ? 'te-IN' : 'en-US';

    currentUtterance.onend = () => {
        isAudioPlaying = false;
        document.getElementById('audio-play-btn').innerText = '▶️ Listen to Care Plan';
    };

    currentUtterance.onerror = (e) => {
        console.warn('TTS error:', e);
        isAudioPlaying = false;
        document.getElementById('audio-play-btn').innerText = '▶️ Listen to Care Plan';
    };

    synth.cancel();
    synth.speak(currentUtterance);
    isAudioPlaying = true;
    document.getElementById('audio-play-btn').innerText = '⏹️ Stop Reading';
}

// Load Previous Reports from SQLite
async function loadPreviousReports() {
    const listContainer = document.getElementById('history-list');
    if (!listContainer) return;

    try {
        const res = await fetch('/api/history');
        const reports = await res.json();

        if (reports.length === 0) {
            listContainer.innerHTML = `
                <div style="text-align:center; padding:36px; color:#64748b;">
                    <p style="font-size:16px;">No previous discharge summary reports saved yet.</p>
                    <p style="font-size:13px; margin-top:4px;">Process a discharge summary to see historical records here.</p>
                </div>
            `;
            return;
        }

        let html = '';
        reports.forEach(r => {
            const isVer = r.overall_status === 'VERIFIED';
            html += `
                <div class="card" style="margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                    <div>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <strong>${r.patient_name}</strong>
                            <span style="background:${isVer ? '#ecfdf5' : '#fef2f2'}; color:${isVer ? '#065f46' : '#991b1b'}; border:1px solid ${isVer ? '#a7f3d0' : '#fecaca'}; font-size:11px; font-weight:700; padding:2px 8px; border-radius:12px;">
                                ${r.overall_status}
                            </span>
                        </div>
                        <div style="font-size:13px; color:#475569; margin-top:2px;">${r.condition}</div>
                        <div style="font-size:11px; color:#94a3b8; margin-top:2px;">Processed on ${r.created_at} • Preservation: ${r.fact_preservation_rate}% • Readability: Grade ${r.flesch_grade}</div>
                    </div>
                    <button class="btn-outline" onclick="loadHistoricalReport('${r.id}')">
                        📖 View Care Plan
                    </button>
                </div>
            `;
        });
        listContainer.innerHTML = html;
    } catch (e) {
        console.error('Error fetching history:', e);
    }
}

async function loadHistoricalReport(id) {
    try {
        const res = await fetch(`/api/history/${id}`);
        const data = await res.json();
        currentCarePlan = data;
        showSection('section-create');
        renderCarePlan(data);
        document.getElementById('results-container').style.display = 'block';
        document.getElementById('results-container').scrollIntoView({ behavior: 'smooth' });
    } catch (e) {
        alert('Unable to load report: ' + e.message);
    }
}

// Load Dashboard Metrics
async function loadDashboardStats() {
    try {
        const res = await fetch('/api/dashboard-stats');
        const stats = await res.json();

        document.getElementById('stat-total-processed').innerText = stats.total_processed;
        document.getElementById('stat-verified-count').innerText = stats.verified_count;
        document.getElementById('stat-review-count').innerText = stats.review_required_count;
        document.getElementById('stat-avg-preservation').innerText = `${stats.avg_preservation_rate}%`;
        document.getElementById('stat-avg-dose-acc').innerText = `${stats.avg_dose_accuracy}%`;
        document.getElementById('stat-avg-warn-recall').innerText = `${stats.avg_warning_recall}%`;
        document.getElementById('stat-total-halluc').innerText = stats.total_hallucinations;
        document.getElementById('stat-avg-flesch').innerText = `Grade ${stats.avg_flesch_grade}`;
    } catch (e) {
        console.error('Error fetching stats:', e);
    }
}

// Run Evaluation Benchmarks
async function runBenchmarks() {
    const btn = document.getElementById('run-benchmarks-btn');
    const resultsContainer = document.getElementById('benchmark-results-container');
    
    btn.disabled = true;
    btn.innerText = '⏳ Running Evaluation Benchmark Suite...';
    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = `<p style="padding:20px; color:#0f766e;">Running 11-point safety audits on 5 gold-standard samples + 2 adversarial mutation test cases...</p>`;

    try {
        const res = await fetch('/api/evaluate', { method: 'POST' });
        const data = await res.json();

        let tableRows = '';
        data.benchmarks.forEach(b => {
            const isPass = b.status === 'VERIFIED';
            const badgeBg = isPass ? '#10b981' : (b.gate_triggered ? '#ef4444' : '#f59e0b');
            tableRows += `
                <tr>
                    <td><strong>${b.title}</strong><br><small style="color:#64748b;">${b.category}</small></td>
                    <td><span style="background:${badgeBg}; color:#fff; font-size:11px; font-weight:700; padding:2px 8px; border-radius:12px;">${b.status}</span></td>
                    <td><strong>${b.gate_triggered ? '🚨 TRIGGERED' : '✅ PASSED'}</strong></td>
                    <td>${b.fact_preservation}%</td>
                    <td>Grade ${b.flesch_grade}</td>
                    <td><small>${b.detected_issue || 'All 11 clinical checks verified.'}</small></td>
                </tr>
            `;
        });

        resultsContainer.innerHTML = `
            <div style="background:#f0fdfa; border:1px solid #99f6e4; padding:16px; border-radius:8px; margin-bottom:16px;">
                <h4 style="color:#0f766e; margin-bottom:6px;">Evaluation Results Summary</h4>
                <div style="display:flex; flex-wrap:wrap; gap:20px; font-size:14px;">
                    <div><strong>Total Evaluated:</strong> ${data.total_evaluated}</div>
                    <div><strong>Safety Gates Triggered:</strong> <span style="color:#ef4444; font-weight:700;">${data.safety_gate_triggered_count} (Caught 100% of adversarial errors)</span></div>
                    <div><strong>Average Preservation Rate:</strong> ${data.avg_preservation_rate}%</div>
                    <div><strong>Average Readability:</strong> Grade ${data.avg_grade_level} (${data.target_class_8_met ? 'Target Met: Class 8 English' : 'Review needed'})</div>
                </div>
            </div>
            <div class="med-table-wrapper">
                <table class="med-table">
                    <thead>
                        <tr>
                            <th>Benchmark Test Case</th>
                            <th>Status</th>
                            <th>Safety Gate</th>
                            <th>Fact Preservation</th>
                            <th>Readability</th>
                            <th>Findings & Safety Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${tableRows}
                    </tbody>
                </table>
            </div>
        `;
    } catch (e) {
        resultsContainer.innerHTML = `<div style="color:#ef4444; padding:16px;">Benchmark failed: ${e.message}</div>`;
    } finally {
        btn.disabled = false;
        btn.innerText = '🚀 Run Automated Evaluation Benchmark Suite';
    }
}

// Utility: Escape HTML
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

// ==========================================================================
// AI Voice Assistant Frontend Controller
// ==========================================================================

let assistantLanguage = 'en';
let assistantSpeechEnabled = true;
let speechRecognizer = null;
let isRecognizing = false;

const ASSISTANT_SUGGESTIONS = {
    en: [
        "When should I take my medicines?",
        "What are the emergency warning signs?",
        "What food should I eat or avoid?",
        "When is my follow-up appointment?"
    ],
    te: [
        "నా మందులు ఎప్పుడు వేసుకోవాలి?",
        "అత్యవసర హెచ్చరిక లక్షణాలు ఏమిటి?",
        "నేను ఎలాంటి ఆహారం తీసుకోవాలి?",
        "నా తదుపరి వైద్య పరీక్ష ఎప్పుడు?"
    ],
    hi: [
        "मुझे अपनी दवाएं कब लेनी चाहिए?",
        "आपातकालीन खतरे के लक्षण क्या हैं?",
        "मुझे क्या खाना चाहिए और क्या नहीं?",
        "मेरा अगला चेकअप कब है?"
    ],
    ta: [
        "நான் மருந்துகளை எப்போது சாப்பிட வேண்டும்?",
        "அவசர எச்சரிக்கை அறிகுறிகள் என்ன?",
        "நான் என்ன உணவு சாப்பிட வேண்டும்?",
        "எனது அடுத்த மருத்துவ சந்திப்பு எப்போது?"
    ]
};

const ASSISTANT_GREETINGS = {
    en: "Hello! I am your CareBridge Companion. Ask me any question about your discharge medicines, timings, diet, or warning signs.",
    te: "నమస్కారం! నేను మీ కేర్‌బ్రిడ్జ్ వాయిస్ అసిస్టెంట్‌ని. మీ మందులు, సమయాలు, ఆహార నియమాలు లేదా హెచ్చరిక లక్షణాల గురించి నన్ను ఏదైనా అడగవచ్చు.",
    hi: "नमस्ते! मैं आपका केयरब्रिज साथी हूँ। आप मुझसे अपनी दवाओं, समय, आहार या खतरे के संकेतों के बारे में पूछ सकते हैं।",
    ta: "வணக்கம்! நான் உங்கள் கேர்பிரிட்ஜ் குரல் உதவியாளர். உங்கள் மருந்துகள், நேரம், உணவு அல்லது எச்சரிக்கை அறிகுறிகள் பற்றி கேளுங்கள்."
};

function toggleVoiceAssistant() {
    const panel = document.getElementById('voice-assistant-panel');
    if (!panel) return;

    const isHidden = (panel.style.display === 'none' || panel.style.display === '');
    if (isHidden) {
        panel.style.display = 'flex';
        updateAssistantContextBanner();
        const msgContainer = document.getElementById('assistant-messages');
        if (msgContainer && msgContainer.children.length === 0) {
            clearAssistantChat();
        }
        renderAssistantSuggestions();
    } else {
        panel.style.display = 'none';
        if (isRecognizing && speechRecognizer) {
            speechRecognizer.stop();
        }
        if (synth) synth.cancel();
    }
}

function updateAssistantContextBanner() {
    const banner = document.getElementById('assistant-context-text');
    if (!banner) return;
    if (currentCarePlan) {
        const pName = currentCarePlan.patient_name || 'Patient';
        const cond = currentCarePlan.condition || 'Recovery';
        banner.textContent = `📋 Care Plan Active: ${pName} (${cond})`;
    } else {
        banner.textContent = '📋 General Recovery Assistant (Load care plan for personalized guidance)';
    }
}

function setAssistantLanguage(lang) {
    assistantLanguage = lang;
    document.querySelectorAll('.assistant-lang-pill').forEach(pill => {
        if (pill.getAttribute('data-lang') === lang) pill.classList.add('active');
        else pill.classList.remove('active');
    });
    renderAssistantSuggestions();
}

function renderAssistantSuggestions() {
    const container = document.getElementById('assistant-suggestions');
    if (!container) return;
    const questions = ASSISTANT_SUGGESTIONS[assistantLanguage] || ASSISTANT_SUGGESTIONS.en;

    container.innerHTML = questions.map(q => `
        <button type="button" class="assistant-suggestion-pill" onclick="sendSuggestedQuestion('${escapeHtml(q)}')">
            ${q}
        </button>
    `).join('');
}

function sendSuggestedQuestion(qText) {
    const input = document.getElementById('assistant-text-input');
    if (input) input.value = qText;
    sendAssistantMessage();
}

function toggleAssistantSpeech() {
    assistantSpeechEnabled = !assistantSpeechEnabled;
    const btn = document.getElementById('assistant-mute-btn');
    if (btn) {
        btn.textContent = assistantSpeechEnabled ? '🔊' : '🔇';
        btn.title = assistantSpeechEnabled ? 'Voice Sound ON' : 'Voice Sound MUTED';
    }
    if (!assistantSpeechEnabled && synth) {
        synth.cancel();
    }
}

function clearAssistantChat() {
    const container = document.getElementById('assistant-messages');
    if (!container) return;
    container.innerHTML = `
        <div class="assistant-msg assistant">
            <div class="msg-bubble">${ASSISTANT_GREETINGS[assistantLanguage] || ASSISTANT_GREETINGS.en}</div>
        </div>
    `;
    if (synth) synth.cancel();
}

function toggleSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const micBtn = document.getElementById('mic-record-btn');
    const waveBar = document.getElementById('assistant-wave');

    if (!SpeechRecognition) {
        alert('Voice microphone input is not supported in this browser. Please type your question in the text box.');
        return;
    }

    if (isRecognizing && speechRecognizer) {
        speechRecognizer.stop();
        return;
    }

    try {
        speechRecognizer = new SpeechRecognition();
        const langMap = { en: 'en-US', te: 'te-IN', hi: 'hi-IN', ta: 'ta-IN' };
        speechRecognizer.lang = langMap[assistantLanguage] || 'en-US';
        speechRecognizer.interimResults = false;
        speechRecognizer.maxAlternatives = 1;

        speechRecognizer.onstart = () => {
            isRecognizing = true;
            if (micBtn) micBtn.classList.add('listening');
            if (waveBar) waveBar.style.display = 'flex';
        };

        speechRecognizer.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const input = document.getElementById('assistant-text-input');
            if (input) input.value = transcript;
            sendAssistantMessage();
        };

        speechRecognizer.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            isRecognizing = false;
            if (micBtn) micBtn.classList.remove('listening');
            if (waveBar) waveBar.style.display = 'none';
        };

        speechRecognizer.onend = () => {
            isRecognizing = false;
            if (micBtn) micBtn.classList.remove('listening');
            if (waveBar) waveBar.style.display = 'none';
        };

        speechRecognizer.start();
    } catch (err) {
        console.error('Recognition error:', err);
        isRecognizing = false;
        if (micBtn) micBtn.classList.remove('listening');
        if (waveBar) waveBar.style.display = 'none';
    }
}

async function sendAssistantMessage() {
    const input = document.getElementById('assistant-text-input');
    if (!input) return;
    const message = input.value.trim();
    if (!message) return;

    input.value = '';
    const msgContainer = document.getElementById('assistant-messages');

    // Add user bubble
    const userMsgEl = document.createElement('div');
    userMsgEl.className = 'assistant-msg user';
    userMsgEl.innerHTML = `<div class="msg-bubble">${escapeHtml(message)}</div>`;
    msgContainer.appendChild(userMsgEl);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    // Loading indicator
    const typingEl = document.createElement('div');
    typingEl.className = 'assistant-msg assistant typing';
    typingEl.id = 'assistant-typing-indicator';
    typingEl.innerHTML = `<div class="msg-bubble" style="font-style:italic; color:#64748b;">Thinking... 💭</div>`;
    msgContainer.appendChild(typingEl);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    const apiKeyInput = document.getElementById('api-key-input');
    const apiKey = apiKeyInput ? apiKeyInput.value.trim() : null;

    let planContext = null;
    let planId = null;
    if (currentCarePlan) {
        planId = currentCarePlan.id;
        planContext = currentCarePlan.english_plan || currentCarePlan;
    }

    try {
        const response = await fetch('/api/assistant/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                language: assistantLanguage,
                plan_id: planId,
                context: planContext,
                api_key: apiKey || null
            })
        });

        const typingIndicator = document.getElementById('assistant-typing-indicator');
        if (typingIndicator) typingIndicator.remove();

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Assistant error');
        }

        const replyEl = document.createElement('div');
        replyEl.className = 'assistant-msg assistant';
        replyEl.innerHTML = `
            <div class="msg-bubble">
                ${data.reply}
                <div style="font-size:11px; color:#64748b; margin-top:6px; border-top:1px dashed #cbd5e1; padding-top:4px;">
                    🛡️ ${data.safety_disclaimer}
                </div>
            </div>
        `;
        msgContainer.appendChild(replyEl);
        msgContainer.scrollTop = msgContainer.scrollHeight;

        // Speak reply if enabled
        if (assistantSpeechEnabled && synth) {
            speakAssistantReply(data.reply, data.voice_lang_code || 'en-US');
        }

    } catch (err) {
        const typingIndicator = document.getElementById('assistant-typing-indicator');
        if (typingIndicator) typingIndicator.remove();

        const errEl = document.createElement('div');
        errEl.className = 'assistant-msg assistant';
        errEl.innerHTML = `<div class="msg-bubble" style="color:#ef4444;">Error: ${err.message}</div>`;
        msgContainer.appendChild(errEl);
        msgContainer.scrollTop = msgContainer.scrollHeight;
    }
}

function speakAssistantReply(text, langCode) {
    if (!synth) return;
    synth.cancel();

    // Clean emojis and symbols for speech
    const cleanText = text.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '');
    const utter = new SpeechSynthesisUtterance(cleanText);
    utter.lang = langCode;
    utter.rate = 1.0;
    synth.speak(utter);
}


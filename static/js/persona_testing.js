/**
 * Persona Testing Module
 * Handles persona selection, API communication, and results visualization
 */

// State management
const PersonaState = {
    selectedPersonas: [],
    allPersonas: [],
    isLoading: false
};

// DOM element references
const PersonaElements = {
    toggleLabel: null,
    section: null,
    toggleIcon: null,
    grid: null,
    count: null,
    selectAllBtn: null,
    clearAllBtn: null
};

/**
 * Initialize persona testing module
 */
function initPersonaTesting() {
    // Get DOM elements
    PersonaElements.toggleLabel = document.getElementById('personaToggleLabel');
    PersonaElements.section = document.getElementById('personaSection');
    PersonaElements.toggleIcon = document.getElementById('personaToggleIcon');
    PersonaElements.grid = document.getElementById('personaGrid');
    PersonaElements.count = document.getElementById('personaCount');
    PersonaElements.selectAllBtn = document.getElementById('selectAllPersonas');
    PersonaElements.clearAllBtn = document.getElementById('clearAllPersonas');
    
    // Setup event listeners
    setupEventListeners();
}

/**
 * Setup all event listeners for persona testing
 */
function setupEventListeners() {
    // Toggle persona section
    if (PersonaElements.toggleLabel) {
        PersonaElements.toggleLabel.addEventListener('click', togglePersonaSection);
    }
    
    // Select/Clear all buttons
    if (PersonaElements.selectAllBtn) {
        PersonaElements.selectAllBtn.addEventListener('click', (e) => {
            e.preventDefault();
            selectAllPersonas();
        });
    }
    
    if (PersonaElements.clearAllBtn) {
        PersonaElements.clearAllBtn.addEventListener('click', (e) => {
            e.preventDefault();
            clearAllPersonas();
        });
    }
}

/**
 * Toggle persona section visibility
 */
function togglePersonaSection() {
    const isVisible = PersonaElements.section.style.display !== 'none';
    PersonaElements.section.style.display = isVisible ? 'none' : 'block';
    PersonaElements.toggleIcon.style.transform = isVisible ? 'rotate(0deg)' : 'rotate(180deg)';
    
    // Load personas on first open
    if (!isVisible && PersonaState.allPersonas.length === 0) {
        loadPersonas();
    }
}

/**
 * Load personas from API
 */
async function loadPersonas() {
    if (PersonaState.isLoading) return;
    
    PersonaState.isLoading = true;
    PersonaElements.grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: var(--space-xl);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">⏳</div>
            Loading personas...
        </div>
    `;
    
    try {
        const response = await fetch('/api/personas');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        // API returns array directly, not wrapped in object
        PersonaState.allPersonas = Array.isArray(data) ? data : (data.personas || []);
        
        if (PersonaState.allPersonas.length === 0) {
            throw new Error('No personas available');
        }
        
        renderPersonaCards();
    } catch (error) {
        console.error('Error loading personas:', error);
        PersonaElements.grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; color: var(--danger); padding: var(--space-xl);">
                <div style="font-size: 2rem; margin-bottom: 1rem;">⚠️</div>
                <div style="margin-bottom: 0.5rem;">Failed to load personas</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">${error.message}</div>
                <button onclick="loadPersonas()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: var(--gradient-primary); border: none; border-radius: 8px; color: white; cursor: pointer;">
                    Retry
                </button>
            </div>
        `;
    } finally {
        PersonaState.isLoading = false;
    }
}

/**
 * Render persona cards in the grid
 */
function renderPersonaCards() {
    if (PersonaState.allPersonas.length === 0) {
        PersonaElements.grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: var(--space-xl);">
                No personas available
            </div>
        `;
        return;
    }
    
    PersonaElements.grid.innerHTML = PersonaState.allPersonas.map(persona => `
        <div class="persona-card" data-persona-id="${persona.id}" onclick="togglePersona('${persona.id}')">
            <div class="persona-card-checkmark">✓</div>
            <span class="persona-card-emoji">${persona.avatar_emoji || '👤'}</span>
            <div class="persona-card-name">${escapeHtml(persona.name)}</div>
            <div class="persona-card-tagline">${escapeHtml(persona.tagline)}</div>
            <div class="persona-card-category">${escapeHtml(persona.category)}</div>
        </div>
    `).join('');
    
    updatePersonaCount();
}

/**
 * Toggle persona selection
 * @param {string} personaId - The ID of the persona to toggle
 */
function togglePersona(personaId) {
    const card = document.querySelector(`[data-persona-id="${personaId}"]`);
    if (!card) return;
    
    const index = PersonaState.selectedPersonas.indexOf(personaId);
    if (index > -1) {
        // Deselect
        PersonaState.selectedPersonas.splice(index, 1);
        card.classList.remove('selected');
    } else {
        // Select
        PersonaState.selectedPersonas.push(personaId);
        card.classList.add('selected');
    }
    
    updatePersonaCount();
}

/**
 * Select all personas
 */
function selectAllPersonas() {
    PersonaState.selectedPersonas = PersonaState.allPersonas.map(p => p.id);
    document.querySelectorAll('.persona-card').forEach(card => {
        card.classList.add('selected');
    });
    updatePersonaCount();
}

/**
 * Clear all persona selections
 */
function clearAllPersonas() {
    PersonaState.selectedPersonas = [];
    document.querySelectorAll('.persona-card').forEach(card => {
        card.classList.remove('selected');
    });
    updatePersonaCount();
}

/**
 * Update persona count display
 */
function updatePersonaCount() {
    const count = PersonaState.selectedPersonas.length;
    PersonaElements.count.textContent = count === 0 ? 'No personas selected' : 
        count === 1 ? '1 persona selected' : 
        `${count} personas selected`;
}

/**
 * Get selected persona IDs
 * @returns {Array<string>} Array of selected persona IDs
 */
function getSelectedPersonas() {
    return PersonaState.selectedPersonas;
}

/**
 * Display persona analysis results
 * @param {Array} personaResults - Array of persona analysis results
 */
function displayPersonaResults(personaResults) {
    const section = document.getElementById('audienceResponseSection');
    const content = document.getElementById('audienceResponseContent');
    
    if (!personaResults || personaResults.length === 0) {
        if (section) section.classList.add('hidden');
        return;
    }
    
    if (section) section.classList.remove('hidden');
    
    // Sort by resonance score
    const sorted = [...personaResults].sort((a, b) => b.resonance_score - a.resonance_score);
    const bestFit = sorted.slice(0, Math.min(3, sorted.length)).map(p => p.persona_id);
    const worstFit = sorted.slice(-Math.min(3, sorted.length)).map(p => p.persona_id);
    
    // Add summary stats
    const avgResonance = sorted.reduce((sum, r) => sum + r.resonance_score, 0) / sorted.length;
    const summaryHtml = `
        <div class="audience-summary">
            <div class="audience-summary-item">
                <div class="audience-summary-value" style="color: var(--success);">${sorted[0] ? Math.round(sorted[0].resonance_score) : '--'}</div>
                <div class="audience-summary-label">Best Fit Score</div>
            </div>
            <div class="audience-summary-item">
                <div class="audience-summary-value" style="color: var(--info);">${Math.round(avgResonance)}</div>
                <div class="audience-summary-label">Average Resonance</div>
            </div>
            <div class="audience-summary-item">
                <div class="audience-summary-value" style="color: var(--text-primary);">${sorted.length}</div>
                <div class="audience-summary-label">Personas Tested</div>
            </div>
        </div>
    `;
    
    content.innerHTML = summaryHtml + sorted.map((result, index) => {
        const isBest = bestFit.includes(result.persona_id);
        const isWorst = worstFit.includes(result.persona_id) && sorted.length > 3;
        
        // Determine fit class based on score
        let fitClass = '';
        if (isBest) {
            fitClass = 'best-fit';
        } else if (isWorst) {
            fitClass = 'worst-fit';
        } else if (result.resonance_score >= 50 && result.resonance_score < 70) {
            fitClass = 'moderate-fit';
        }
        
        return createPersonaResultCard(result, index, isBest, isWorst, fitClass);
    }).join('');
    
    // Animate bars after render
    setTimeout(() => {
        document.querySelectorAll('.persona-result-bar-fill').forEach(bar => {
            const width = bar.getAttribute('data-width');
            bar.style.width = width + '%';
        });
    }, 100);
}

/**
 * Create HTML for a persona result card
 */
function createPersonaResultCard(result, index, isBest, isWorst, fitClass) {
    const fitBadge = isBest ? '<span style="color: var(--success); margin-left: 8px; font-size: 0.9rem;">✓ Best Fit</span>' : 
                     isWorst ? '<span style="color: var(--danger); margin-left: 8px; font-size: 0.9rem;">⚠ Low Fit</span>' : 
                     fitClass === 'moderate-fit' ? '<span style="color: var(--warning); margin-left: 8px; font-size: 0.9rem;">~ Moderate</span>' : '';
    
    return `
        <div class="persona-result-item ${fitClass}" 
             style="animation: alertSlide 0.5s ease-out ${index * 0.1}s backwards;">
            <div class="persona-result-header">
                <span class="persona-result-emoji">${result.avatar_emoji || '👤'}</span>
                <div class="persona-result-info">
                    <div class="persona-result-name">
                        ${escapeHtml(result.persona_name)}
                        ${fitBadge}
                    </div>
                    <div class="persona-result-tagline">${escapeHtml(result.tagline || '')}</div>
                </div>
                <div class="persona-result-score">
                    <div class="persona-result-score-value">
                        ${Math.round(result.resonance_score)}
                    </div>
                    <div class="persona-result-score-label">Resonance</div>
                </div>
            </div>
            <div class="persona-result-details">
                <div class="persona-result-detail">
                    <span class="persona-result-detail-icon">😊</span>
                    <div class="persona-result-detail-text">
                        <div class="persona-result-detail-label">Dominant Emotion</div>
                        <div class="persona-result-detail-value">${escapeHtml(result.dominant_emotion || 'Neutral')}</div>
                    </div>
                </div>
                <div class="persona-result-detail">
                    <span class="persona-result-detail-icon">🎯</span>
                    <div class="persona-result-detail-text">
                        <div class="persona-result-detail-label">Likely Action</div>
                        <div class="persona-result-detail-value">${escapeHtml(result.most_likely_action || 'View')}</div>
                    </div>
                </div>
                <div class="persona-result-detail">
                    <span class="persona-result-detail-icon">💚</span>
                    <div class="persona-result-detail-text">
                        <div class="persona-result-detail-label">Engagement Likelihood</div>
                        <div class="persona-result-bar">
                            <div class="persona-result-bar-fill" 
                                 data-width="${result.engagement_likelihood || 0}" 
                                 style="width: 0%;"></div>
                        </div>
                    </div>
                </div>
                <div class="persona-result-detail">
                    <span class="persona-result-detail-icon">🔄</span>
                    <div class="persona-result-detail-text">
                        <div class="persona-result-detail-label">Share Likelihood</div>
                        <div class="persona-result-bar">
                            <div class="persona-result-bar-fill" 
                                 data-width="${result.share_likelihood || 0}" 
                                 style="width: 0%;"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export functions for use in main script
window.PersonaTesting = {
    init: initPersonaTesting,
    getSelectedPersonas: getSelectedPersonas,
    displayResults: displayPersonaResults,
    loadPersonas: loadPersonas
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPersonaTesting);
} else {
    initPersonaTesting();
}

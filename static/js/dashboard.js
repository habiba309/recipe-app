/**
 * dashboard.js — Pure UI helpers only.
 * No fetch, no API calls, no localStorage, no business logic.
 * All data is submitted via standard HTML multipart/form POST to Django views.
 */

// ─── Image preview ───────────────────────────────────────────
const imgInput = document.getElementById('id_image');

if (imgInput) {
    imgInput.addEventListener('change', function () {
        const file = this.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            alert('Please select an image file (JPG or PNG).');
            this.value = '';
            return;
        }

        if (file.size > 2 * 1024 * 1024) {
            alert('Image must be smaller than 2 MB.');
            this.value = '';
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            const preview  = document.getElementById('previewImage');
            const upLabel  = document.getElementById('uploadContent');

            if (preview) {
                preview.src           = e.target.result;
                preview.style.display = 'block';
            }
            if (upLabel) {
                upLabel.style.display = 'none';
            }
        };
        reader.readAsDataURL(file);
    });
}

// ─── Ingredient rows (UI only — data posted as arrays) ────────

/**
 * Remove an ingredient row.
 * Keeps at least one row so the server-side check can report the error.
 */
function removeIng(btn) {
    const container = document.getElementById('ingredientsContainer');
    if (!container) return;

    const rows = container.querySelectorAll('.ing-row');
    if (rows.length <= 1) {
        alert('At least one ingredient is required.');
        return;
    }
    btn.closest('.ing-row').remove();
}

/**
 * Append a new ingredient row to the container.
 * @param {string} name  - pre-fill name value (optional)
 * @param {string} qty   - pre-fill quantity value (optional)
 */
function addIngRow(name, qty) {
    const container = document.getElementById('ingredientsContainer');
    if (!container) return;

    const row = document.createElement('div');
    row.className = 'ing-row';
    row.innerHTML =
        '<input type="text" name="ingredient_name" placeholder="Ingredient name"' +
            ' value="' + (name || '') + '" required>' +
        '<input type="text" name="ingredient_quantity" placeholder="Quantity"' +
            ' value="' + (qty  || '') + '">' +
        '<button type="button" class="rem-ing" onclick="removeIng(this)" title="Remove">' +
            '<i class="fa-solid fa-trash"></i>' +
        '</button>';

    container.appendChild(row);
    row.querySelector('input').focus();
}

// Wire up "Add Ingredient" button
const addIngBtn = document.getElementById('addIngBtn');
if (addIngBtn) {
    addIngBtn.addEventListener('click', function () {
        addIngRow('', '');
    });
}

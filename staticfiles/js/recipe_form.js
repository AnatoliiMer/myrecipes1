document.addEventListener('DOMContentLoaded', function() {
    const ingredientForms = document.getElementById('ingredient-forms');
    const addIngredientButton = document.getElementById('add-ingredient');
    const totalForms = document.getElementById('id_ingredients-TOTAL_FORMS');
    const formPrefix = 'ingredients';

    let formCount = parseInt(totalForms.value);

    addIngredientButton.addEventListener('click', function() {
        const newForm = document.createElement('div');
        newForm.classList.add('ingredient-form', 'mb-3');
        newForm.innerHTML = `
            <div class="row ingredient-row">
                <div class="col-md-6 form-group">
                    <label for="id_${formPrefix}-${formCount}-name" class="form-label">${gettext('Название ингредиента')}</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-list"></i></span>
                        <input type="text" name="${formPrefix}-${formCount}-name" class="form-control" id="id_${formPrefix}-${formCount}-name">
                    </div>
                </div>
                <div class="col-md-6 form-group">
                    <label for="id_${formPrefix}-${formCount}-quantity" class="form-label">${gettext('Количество')}</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-balance-scale"></i></span>
                        <input type="text" name="${formPrefix}-${formCount}-quantity" class="form-control" id="id_${formPrefix}-${formCount}-quantity">
                    </div>
                </div>
            </div>
            <div class="form-check delete-ingredient-checkbox">
                <input type="checkbox" name="${formPrefix}-${formCount}-DELETE" class="form-check-input" id="id_${formPrefix}-${formCount}-DELETE">
                <label for="id_${formPrefix}-${formCount}-DELETE" class="form-check-label">${gettext('Удалить ингредиент')}</label>
            </div>
            <input type="hidden" name="${formPrefix}-${formCount}-id" id="id_${formPrefix}-${formCount}-id">
        `;
        ingredientForms.appendChild(newForm);
        formCount++;
        totalForms.value = formCount;
    });
});
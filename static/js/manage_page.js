function selectAll(){
    let selectAll = document.getElementById('select-all');
    let selectOnes = document.getElementsByClassName('select-one');
    for (let i = 0; i < selectOnes.length; i++) {
        // traverse through all checkbox, assign the value of
        // check-all checkbox to each single checkbox.
        selectOnes[i].checked = selectAll.checked;
    }
}

function selectOne(){
    let selectAll = document.getElementById('select-all');
    let selectOnes = document.getElementsByClassName('select-one');
    let isAllChecked = true;
    for (let i = 0; i < selectOnes.length; i++) {
        if (selectOnes[i].checked === false) {
            isAllChecked = false;
            break;
        }
    }
    selectAll.checked = isAllChecked;
}

function submitForm(id){
    document.getElementById(id).submit();
}

function setValues(id, name, cate, unit, spec, desc){
    document.getElementById("alt_com_id").value = id
    document.getElementById("alt_com_name").value = name
    let cate_select = document.getElementById("alt_com_cate")
    let unit_select = document.getElementById("alt_com_unit")
    for (let i = 0; i < cate_select.length; i++){
        if (cate_select[i].value === cate){
            cate_select[i].selected = true
        }
    }
    for (let i = 0; i < unit_select.length; i++){
        if (unit_select[i].value === unit){
            unit_select[i].selected = true
        }
    }
    document.getElementById("alt_com_spec").value = spec
    document.getElementById("alt_com_desc").value = desc
}

(function () {

    let forms = document.querySelectorAll('.needs-validation')

        Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
})()

function search_all(){
    document.getElementById("search_com_cate").value = "ALL"
    document.getElementById("search_com_id").value = "ALL"
    document.getElementById("search_com_name").value = "ALL"
    let form = document.getElementById("search-form")
    form.submit()
}

function disable_search(){

    document.getElementById("search-form-submit").disabled = !(document.getElementById("search_com_name").value ||
        document.getElementById("search_com_id").value ||
        document.getElementById("search_com_cate").value);

}

function switch_stock_alerts(){
    document.getElementById("stock_alerts").disabled = !document.getElementById("stock_alerts").disabled
    if (!document.getElementById("stock_alerts").disabled) {
        document.getElementById("stock_alerts_aster").innerText = "*"
        document.getElementById("stock_alerts").required = true
    }
    else {
        document.getElementById("stock_alerts_aster").innerText = ""
        document.getElementById("stock_alerts").required = false
    }
}




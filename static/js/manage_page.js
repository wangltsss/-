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

function setValues(id, name, desc, cate, unit, spec){
    alert(id.toString())
    alert(name.toString())
    alert(unit.toString())
    alert(cate.toString())
    alert(spec.toString())
    alert(desc.toString())
    /*
    let id = item[0]
    let name = item[1]
    let cate = item[3]
    let unit = item[4]
    let spec = item[5]
    let desc = item[2]
    document.getElementById("alt_com_id").value = id
    document.getElementById("alt_com_name").value = name
    document.getElementById("alt_com_cate").value = cate
    document.getElementById("alt_com_unit").value = unit
    document.getElementById("alt_com_spec").value = spec
    document.getElementById("alt_com_desc").value = desc
    */
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










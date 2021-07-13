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

/*
function getId(){
    let records = document.getElementsByName("s-record");
    let ls_id = [];
    for (let i = 0; i < records.length; i++) {
        if (records[i].checked) {
            ls_id.push(records[i])
        }
    }
    return ls_id
}
*/

function submitForm(id){
    document.getElementById(id).submit();
}

/*
function showToast(cls){
    let toasts = document.getElementsByClassName(cls);
    for (let i = 0; i < toasts.length; i++) {
        i = 1;
    }
}
*/













"use strict"

function toggle_visible(id){
    let ele = document.getElementById(id)
    ele.style.display = "block";
}

function toggle_invisible(id){
    let ele = window.parent.document.getElementById(id)
    ele.style.display = "none";
}

function toggle_visibility(id){
    for (let i = 0; i < subpages.length; i++){
        if (subpages[i][0] === id){
            toggle_visible(id)
            let cls = document.getElementById(subpages[i][1]).getAttribute("class")
            if (cls.indexOf(" active") === -1) {
                cls = cls.concat(" active")
            }
            document.getElementById(subpages[i][1]).setAttribute("class", cls)

        }
        else{
            toggle_invisible(subpages[i][0])
            let cls = document.getElementById(subpages[i][1]).getAttribute("class")
            cls = cls.replace(" active", "")
            document.getElementById(subpages[i][1]).setAttribute("class", cls)
        }
    }
}

const subpages =
    [['commodity_wrapper', 'cm_page'], ['stock_wrapper', 'sm_page'],
    ['stock_in_wrapper', 'si_page'], ['stock_out_wrapper', 'so_page'],
    ['setting_page', '']];




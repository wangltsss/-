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
        if (subpages[i] === id){
            toggle_visible(id)
        }
        else{
            toggle_invisible(subpages[i])
        }
    }
}

const subpages =
    ['commodity_wrapper', 'stock_wrapper',
    'stock_in_wrapper', 'stock_out_wrapper',
    'setting_page'];




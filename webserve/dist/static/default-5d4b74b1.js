import{b as i}from"./index-2c1993c2.js";var s=function(a,o){var t=i({},a);return Object.keys(o).forEach(function(r){var e=t[r];if(e)e.type||e.default?e.default=o[r]:e.def?e.def(o[r]):t[r]={type:e,default:o[r]};else throw new Error("not have ".concat(r," prop"))}),t};const l=s;var n=Symbol("siderCollapsed"),d=Symbol("siderHookProvider");export{d as S,n as a,l as i};
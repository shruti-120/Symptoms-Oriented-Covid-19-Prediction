var ann_graphs = document.getElementById('knn');
var visual_graphs = document.getElementById('visual');
var rfc_graphs = document.getElementById('rfc');
var lstm_graphs = document.getElementById('svm');
var naive_graphs = document.getElementById('navy');



function ann(){
ann_graphs.style.display='block';
rfc_graphs.style.display='none';
visual_graphs.style.display='none';
lstm_graphs.style.display='none';
naive_graphs.style.display='none';
}

function rfc(){
rfc_graphs.style.display='block';
ann_graphs.style.display='none';
visual_graphs.style.display='none';
lstm_graphs.style.display='none';
naive_graphs.style.display='none';
}

function visual(){
visual_graphs.style.display='block';
ann_graphs.style.display='none';
rfc_graphs.style.display='none';
lstm_graphs.style.display='none';
naive_graphs.style.display='none';
}

function lstm(){
ann_graphs.style.display='none';
rfc_graphs.style.display='none';
visual_graphs.style.display='none';
lstm_graphs.style.display='block';
naive_graphs.style.display='none';
}

function navy(){
ann_graphs.style.display='none';
rfc_graphs.style.display='none';
visual_graphs.style.display='none';
lstm_graphs.style.display='none';
naive_graphs.style.display='block';
}


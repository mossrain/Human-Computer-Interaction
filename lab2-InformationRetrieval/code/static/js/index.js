const uploadBox = document.getElementById('upload-box');
const preview = document.getElementById('preview');
const uploadInput = document.getElementById('upload-input');
const uploadText = document.getElementById('upload-text');
var passFile = null;
const clear = document.getElementById('clear');

//初始化多选框
const tagList = ['animals', 'baby', 'bird', 'car', 'clouds', 'dog', 'female', 'flower', 'food', 'indoor', 'lake', 'male', 'night', 'people', 'plant', 'portrait', 'river', 'sea', 'sky', 'structures', 'sunset', 'transport', 'tree', 'water'];
const tagContainer = document.getElementById('dropdown-content');
// 添加tagContainer子元素
tagList.forEach(tag => {
  const tagElement = document.createElement('label');
  //设置tagElement的id
  tagElement.setAttribute('id', tag);
  //将label的innerHTML设置为tag
  tagElement.innerHTML = tag;
  //使用tagElement成为tagContainer的子元素
  tagContainer.appendChild(tagElement);

  //添加label的子元素
  const inputElement = document.createElement('input');
  inputElement.setAttribute('type', 'checkbox');
  inputElement.setAttribute('name', 'tag');
  inputElement.setAttribute('value', tag);
  //将input 设置为默认Selected
  inputElement.setAttribute('checked', 'checked');


  //使用inputElement成为tagElement的子元素
  tagElement.appendChild(inputElement);

  });

clear.addEventListener('click', () => {
  //刷新頁面
  console.log("刷新");
  window.location.reload();
});


uploadBox.addEventListener('dragover', (event) => {
  event.preventDefault();
  uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
  uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (event) => {
  event.preventDefault();
  uploadBox.classList.remove('dragover');
  const files = event.dataTransfer.files;
  if (files.length > 0) {
    console.log('dropped');
    const file = files[0];
    console.log(file.type);
    if (file.type.startsWith('image/')) {
      passFile = file;
      const reader = new FileReader();
      reader.onload = (event) => {
        preview.src = event.target.result;
        // preview.style.display = 'inline-block';
        // 让preview作为背景图填满整个uploadBox
        uploadBox.style.backgroundImage = `url(${event.target.result})`;
        uploadBox.style.backgroundSize = 'cover';
        uploadBox.style.backgroundPosition = 'center';
        uploadText.style.display = 'none';

      };
      reader.readAsDataURL(file);
      console.log(file);
      // TODO: 上传文件到服务器
    } else {
      alert('只能上传图片文件');
    }
  }
});

uploadBox.addEventListener('click', () => {
  const uploadInput = document.getElementById('upload-input');
  uploadInput.click();
});


uploadInput.addEventListener('change', () => {
  
  const file = uploadInput.files[0];
  passFile = file;
  console.log('change');
  if (file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = (event) => {
      preview.src = event.target.result;
      // preview.style.display = 'inline-block';
       // 让preview作为背景图填满整个uploadBox
      uploadBox.style.backgroundImage = `url(${event.target.result})`;
      uploadBox.style.backgroundSize = 'cover';
      uploadBox.style.backgroundPosition = 'center';
      uploadText.style.display = 'none';
    };
    reader.readAsDataURL(file);
    console.log('成功收到图片',file);
    // TODO: 上传文件到服务器
  } else {
    alert('只能上传图片文件');
  }

   // 上传完成后，清空 input 的值，以便用户重新选择同一个文件时，能够触发 change 事件。
   uploadInput.value = '';
});


//保存和不喜欢
// 获取所有的图片容器
const imageContainers = document.querySelectorAll('.search-result');

// 遍历每个图片容器
imageContainers.forEach(container => {
  // 获取当前容器下的图片元素
  const image = container.querySelector('img');

  // 创建保存图标元素
  const saveIcon = document.createElement('span');
  saveIcon.classList.add('icon', 'save');
  saveIcon.addEventListener('click', () => {
    // 创建一个a标签，用于下载图片
    const link = document.createElement('a');
    link.href = image.src;
    link.download = 'image.jpg';
    link.click();
  });

  // 创建不喜欢图标元素
  const dislikeIcon = document.createElement('span');
  dislikeIcon.classList.add('icon', 'dislike');
  dislikeIcon.addEventListener('click', () => {
    // 输出图片路径到控制台
    console.log(image.src);
    //修改class="dislike-tooltip"的display属性
    var tooltip = container.querySelector('.dislike-tooltip');
    tooltip.style.display = 'block';
    tooltip.style.color = 'white';
    //背景色设为半透明的黑色
    tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    //父节点设为半透明
    tooltip.parentNode.style.opacity = '0.5';
    // tooltipSibling.style.visibility = 'hidden';
    //将不喜欢图片的路径传给后端
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/dislike", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ "dislike": image.src }));
    // console.log(image.src);

  });

  //如果点击search，不喜欢提示框消失
  var search = document.getElementById("search");
  search.addEventListener('click', () => {
    var tooltip = container.querySelector('.dislike-tooltip');
    tooltip.style.display = 'none';
    tooltip.parentNode.style.opacity = '1';
  });

  // 创建覆盖层元素
  const overlay = document.createElement('div');
  overlay.classList.add('overlay');
  overlay.appendChild(saveIcon);
  overlay.appendChild(dislikeIcon);

  // 将覆盖层元素添加到图片容器中
  container.appendChild(overlay);

});

//获取id为'select-num'的select组件的值
function getSelectValue(){
  var select = document.getElementById("select-num");
  var selectedValue = select.options[select.selectedIndex].value;
  console.log(selectedValue);

  //对classname为'search-result'的元素进行操作
  var searchResult = document.getElementsByClassName("search-result");
  console.log(searchResult);
  for(var i=0;i<searchResult.length;i++){
    //先全部隐藏
    searchResult[i].style.display = "none";
  }
  for(var i=0;i<selectedValue;i++){
    //再显示前selectedValue个
    searchResult[i].style.display = "block";
  }

  return selectedValue;
}

function myFunction(){

	document.getElementById("predictedResult").innerHTML= "";
	$('#clear').hide();
}

function moveComponent() {
  // var component = document.getElementById("main");
  // component.style.marginRight = "50vw";

  // var search = document.getElementById("search");
  // search.style.display = "none";

  var clear = document.getElementById("clear");
  clear.style.display = "block";

}


// function clear(){
//   //刷新頁面
//   console.log("刷新");
//   window.location.reload();
// }
function toggleDropdown() {
  const dropdownContent = document.getElementById("dropdown-content");
  dropdownContent.classList.toggle("show");
  //如果下拉列表显示，则将按钮文字改为“完成选择”，否则改为“选择标签”
  if (dropdownContent.classList.contains("show")) {
    document.querySelector(".dropdown-btn").innerText = 'Choose the tags';
  } else {
    updateButtonText();
  }
}


// 获取复选框的选中状态
function getCheckedValues() {
  const checkboxes = document.querySelectorAll(".dropdown-content input[type='checkbox']");
  const checkedValues = Array.from(checkboxes)
    .filter((checkbox) => checkbox.checked)
    .map((checkbox) => checkbox.value);
  return checkedValues;
}

// 当下拉列表中的任何复选框被选中或取消选中时，更新选中状态
const checkboxes = document.querySelectorAll(".dropdown-content input[type='checkbox']");
checkboxes.forEach(checkbox => {
  checkbox.addEventListener("change", function() {
    const isChecked = this.checked;
    const label = this.parentNode;
    label.classList.toggle("selected", isChecked);
    // updateButtonText();
    document.querySelector(".dropdown-btn").innerText = 'Choose the tags';
  });
});

// 更新按钮文本以显示选中的选项
function updateButtonText() {
  const selectedLabels = document.querySelectorAll(".dropdown-content .selected");
  // const selectedOptions = Array.from(selectedLabels).map(label => label.innerText);
  // console.log(selectedOptions);
  const selectedOptions = getCheckedValues();
  const buttonText = selectedOptions.length > 0 ? 'Selected: '+selectedOptions.join(", ") : "Choose the tags";
  document.querySelector(".dropdown-btn").innerText = buttonText;
}

// 当用户单击页面上的任何位置时，如果下拉列表可见，则关闭下拉列表
window.addEventListener("click", function(event) {
  const dropdownContent = document.getElementById("dropdown-content");
  const dropdownBtn = document.querySelector(".dropdown-btn");
  if (event.target !== dropdownBtn && !dropdownContent.contains(event.target)) {
    dropdownContent.classList.remove("show");
    updateButtonText();
  }
});


async function fun(){
    console.log('into fun');

    

    // 检验是否上传图片
    if (passFile == null) {
      alert('请上传图片');
      return;
    }
    else{
      console.log('上传图片成功');
      $('#load').show();
      console.log(passFile);

      //通过ajax将图片传到后端
      var formData = new FormData();
      formData.append('file', passFile);
      console.log('formData1',formData);

      //将选择的tags传到后端
      var selectedOptions = getCheckedValues();
      console.log(selectedOptions);
      list=JSON.stringify(selectedOptions);
      formData.append('list', list);
      console.log('formData2',formData);


      $.ajax({
        url: 'imgUpload',
        type: 'POST',
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,

        success: function (response) {
              moveComponent();
              $('#load').hide();
              $('#row1').show();
              // document.getElementById("results").style.display = "block";
              $('#results').show();
              
              document.getElementById("img0").src = response.image0;
              document.getElementById("img1").src = response.image1;
              document.getElementById("img2").src = response.image2;
              document.getElementById("img3").src = response.image3;
              document.getElementById("img4").src = response.image4;
              document.getElementById("img5").src = response.image5;
              document.getElementById("img6").src = response.image6;
              document.getElementById("img7").src = response.image7;
              document.getElementById("img8").src = response.image8;
              document.getElementById("img9").src = response.image9;
              document.getElementById("img10").src = response.image10;
              document.getElementById("img11").src = response.image11;

              document.getElementById("sim0").innerHTML = "Similarity:"+response.sim0+"%";
              document.getElementById("sim1").innerHTML = "Similarity:"+response.sim1+"%";
              document.getElementById("sim2").innerHTML = "Similarity:"+response.sim2+"%";
              document.getElementById("sim3").innerHTML = "Similarity:"+response.sim3+"%";
              document.getElementById("sim4").innerHTML = "Similarity:"+response.sim4+"%";
              document.getElementById("sim5").innerHTML = "Similarity:"+response.sim5+"%";
              document.getElementById("sim6").innerHTML = "Similarity:"+response.sim6+"%";
              document.getElementById("sim7").innerHTML = "Similarity:"+response.sim7+"%";
              document.getElementById("sim8").innerHTML = "Similarity:"+response.sim8+"%";
              document.getElementById("sim9").innerHTML = "Similarity:"+response.sim9+"%";
              document.getElementById("sim10").innerHTML = "Similarity:"+response.sim10+"%";
              document.getElementById("sim11").innerHTML = "Similarity:"+response.sim11+"%";

              // $('#table').show();
              getSelectValue();
              $('#clear').show();
              console.log('success in fun()');
        },

        error: function(response) {
          console.log("Error: " + response);
          alert("api请求失败！");
          $('#load').hide();
          $('#clear').show();
        }
    });

        // return false;   
    }
  };

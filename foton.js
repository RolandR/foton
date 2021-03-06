var currentlyDisplayed = null;

function showPhoto(element){
	var imageName = element.dataset.image;

	display(imageName);
	
	document.getElementById("overlay").style.display = "block";
	setTimeout(function(){
		document.getElementById("overlay").style.opacity = 1;
	}, 10);
	
}

function closeOverlay(){
	document.getElementById("overlay").style.opacity = 0;
	setTimeout(function(){
		document.getElementById("overlay").style.display = "none";
	}, 250);
	
}

function display(file){

	var img = document.getElementById("mainImage");
	
	currentlyDisplayed = file;
	
	var srcset = "PATHpx800/FILE 800w,\
				  PATHpx1200/FILE 1200w,\
				  PATHpx1600/FILE 1600w,\
				  PATHpx2000/FILE 2000w";

	var src = "PATHpx800/FILE";

	srcset = srcset.replace(/PATH/g, metadata.path);
	srcset = srcset.replace(/FILE/g, file);

	src = src.replace(/PATH/g, metadata.path);
	src = src.replace(/FILE/g, file);

	img.srcset = "";
	img.src = "";

	img.srcset = srcset;
	img.src = src;

	document.getElementById("xofy").innerHTML = "Image "+(getImageIndex(file)+1)+" of "+metadata.images.length;
	document.getElementById("originalImage").href = metadata.path + file;
	document.getElementById("imageSize").innerHTML = getImageMetadata(file).size;
}

function next(){
	var index = getImageIndex(currentlyDisplayed);
	var imageCount = metadata.images.length;
	var nextIndex = (index + 1) % imageCount;

	var nextImage = metadata.images[nextIndex].file;
	display(nextImage);
}

function previous(){
	var index = getImageIndex(currentlyDisplayed);
	var imageCount = metadata.images.length;
	var previousIndex = (index - 1 + imageCount) % imageCount;

	var previousImage = metadata.images[previousIndex].file;
	display(previousImage);
}

function getImageMetadata(imageName){
	for(var i = 0; i < metadata.images.length; i++){
		if(metadata.images[i].file == imageName){
			return metadata.images[i];
		}
	}
}

function getImageIndex(imageName){
	for(var i = 0; i < metadata.images.length; i++){
		if(metadata.images[i].file == imageName){
			return i;
		}
	}
}

window.addEventListener("keyup", function(e){
	switch(e.key){
		case "ArrowRight":
		case "L":
		case "D":
			next();
		break;
		case "ArrowLeft":
		case "H":
		case "A":
			previous();
		break;
		case "Escape":
			closeOverlay();
		break;
	}
});

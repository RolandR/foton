
function showPhoto(element){
	var imageName = element.dataset.image;

	var srcset = "PATH/px800/FILE 800w,\
				  PATH/px1200/FILE 1200w,\
				  PATH/px1600/FILE 1600w,\
				  PATH/px2000/FILE 2000w";

	var src = "PATH/px800/FILE";

	srcset = srcset.replace(/PATH/g, metadata.path);
	srcset = srcset.replace(/FILE/g, imageName);

	src = src.replace(/PATH/g, metadata.path);
	src = src.replace(/FILE/g, imageName);

	document.getElementById("mainImage").srcset = srcset;
	document.getElementById("mainImage").src = src;
	document.getElementById("overlay").style.display = "block";
	setTimeout(function(){
		document.getElementById("overlay").style.opacity = 1;
	}, 10);
	
}

function getImageMetadata(imageName){
	for(var i = 0; i < metadata.images.length; i++){
		if(images[i].file == imageName){
			return images[i];
		}
	}
}

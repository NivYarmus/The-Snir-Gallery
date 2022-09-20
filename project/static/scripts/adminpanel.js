function Preview(uploadID, previewID)
{
    let oFReader = new FileReader();
    oFReader.readAsDataURL(document.getElementById(uploadID).files[0]);

    oFReader.onload = function (oFReader)
    {
        document.getElementById(previewID).src = oFReader.target.result;
    };
};
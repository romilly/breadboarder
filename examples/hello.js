module.exports = function (inputParams) {
  return {
    contentType: 'text/html',
    content: `<html><body>
     <div>
     <img src="${inputParams.filename}"
     </div>`
  };
};
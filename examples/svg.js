const path = require('path');


module.exports = function (inputParams) {
  return {
    contentType: 'text/html',
    content: `<html><body>
     <div>
     <img src="file:///${path.resolve(inputParams.filename)}"/>
     </div>`
  };
};
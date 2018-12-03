<!DOCTYPE html>
<link href="https://fonts.googleapis.com/css?family=Lobster" rel="stylesheet" type="text/css">
<style>
  	h1 {
    		font-family: Lobster, Monospace;
		color: green;
		text-align: center;
  	}
	.title-size {
	    	font-size: 50px;
  	}
  	.is-Transformed {   
  		width: 50%;  
 		margin: auto;  
  		position: absolute;  
		top: 50%; left: 50%;  
  		-webkit-transform: translate(-50%,-50%);  
      		-ms-transform: translate(-50%,-50%);  
        	transform: translate(-50%,-50%);  
	.oneline {
		display: inline;
	}  
  	
	input{
    		border: none;
		padding: 10px;
		margin: 10px;
		height: 20px;
    		width: 500px;
		border:1px solid #eaeaea;
		outline:none;
	}
	
	input:hover{
		border-color: #a0a0a0 #b9b9b9 #b9b9b9 #b9b9b9;
	}
	
	input:focus{
		border-color:#4d90fe;
	}

	input[type="submit"] {
		border-radius: 2px;
		background: #f2f2f2;
		border: 1px solid #f2f2f2;
		color: #757575;
		cursor: default;
		font-size: 14px;
		font-weight: bold;
		width: 100px;
		padding: 0 16px;
		height:36px;
	}
	input[type="submit"]:hover {
		box-shadow: 0 1px 1px rgba(0,0,0,0.1);
		background: #f8f8f8;
		border: 1px solid #c6c6c6;
		box-shadow: 0 1px 1px rgba(0,0,0,0.1);
		color: #222;
	}
	.search-div {
		text-align: center;
	<!-Pagination Related ->	
	.pagination {
    display: inline-block;
}

.pagination a {
    color: black;
    float: left;
    padding: 8px 16px;
    text-decoration: none;
    transition: background-color .3s;
    border: 1px solid #ddd;
}

.pagination a.active {
    background-color: #4CAF50;
    color: white;
    border: 1px solid #4CAF50;
}

.pagination a:hover:not(.active) {background-color: #ddd;}
</style>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Autocomplete - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
  <link rel="stylesheet" href="/resources/demos/style.css">
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  <script>
  $( function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme",
	  "Toronto",
	  "eecg",
	  "map",
	  "CSC",
	  "326",
	  "Project"
    ];
    $( "#Search" ).autocomplete({
      source: availableTags
    });
  } );
  </script>
</head>
	<div class="is-Transformed">
		<h1 class="title-size">GreenLight</h1>	
		<div align="center">
		 <form action ="/search" method="get">
         	<input id='Search' name="keywords" type="text"/>
			<input value = "Search" type="submit"/>
        </form>
		</div>
	</div>

<div id="results">
<table id="resultsTable" >
    %for x in range(len(urlList)):
    <tr>
        <td>
        <a href="{{urlList[x][0]}}">{{urlList[x][0]}}</a>
    </tr>
    %end
</table>

</div>
        %if len(urlList)==0:
           <p> No Results Found.</p>
        </td>
        %end
<div id="pages" align="left">

<table class="oneline search-div">
	<tr>
	<!-- <td><a href="#" class="pagination">previous</a></td> -->
	%for x in range(1,int(ctrlList[-2]+1)):
		%url_line=ctrlList[0]
		%for i in range(1,len(ctrlList)-2):
			%url_line+="+"+ctrlList[i]
		%end
		%whole_line="/search/"+url_line
        <td class="pagination"><a href="{{whole_line}}/{{x}}">{{x}}</a></td>
    %end
	<!-- <td><a href="#" class="pagination">next</a></td> -->
	</tr>
</table>
</div>



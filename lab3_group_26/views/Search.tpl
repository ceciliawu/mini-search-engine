<!DOCTYPE html>
<link href="https://fonts.googleapis.com/css?family=Lobster" rel="stylesheet" type="text/css">
<style>
  	h1 {
    		font-family: Lobster, Monospace;
		color: green;
		text-align: center;
  	}
	.title-size {
	    	font-size: 100px;
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
	}
</style>
	<div class="is-Transformed">
		<h1 class="title-size">GreenLight</h1>	
		<div align="center">
		 <form action ="/search" method="get">
         	<input name="keywords" type="text"/>
         	<input value = "Search" type="submit"/>
        </form>
		</div>
	</div>
		
	<div class="right">
		% if user_email: # if user is signed in
				<p style="text-align: center;">{{user_name}}</p>
				<img style="display:block; margin: auto;" src="{{user_pic}}" alt="profile pic" height="30">
			<p style="color:blue;">{{user_email}}</p>
			<a href="/logout">Logout</a>
		% else: # user is not logged in
			<p><a href="/home">Google Login</a></p>
		% end
	</div>
<br>

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
	%for x in range(1,int(ctrlList[1]+1)):
            <td class="pagination"><a href="/search/{{ctrlList[0]}}/{{x}}">{{x}}</a></td>
    %end
	<!-- <td><a href="#" class="pagination">next</a></td> -->
	</tr>
</table>
</div>



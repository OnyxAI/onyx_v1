document.addEventListener('DOMContentLoaded', function () {

		var etape1 = document.getElementById('etape1');
		var etape2 = document.getElementById('etape2');
		etape1.addEventListener('click', save_step_1);
		etape2.addEventListener('click', save_step_2);

		var gostep1 = document.getElementById('gostep1');
		var gostep2 = document.getElementById('gostep2');
		var gostep3 = document.getElementById('gostep3');
		gostep1.addEventListener('click', gotostep1);
		gostep2.addEventListener('click', gotostep2);	
		gostep3.addEventListener('click', gotostep3);	

});

var current_step = 1;

function save_step_1()
{
	
   change_step(1,2); 
	 current_step = 2;

}

function save_step_2()
{
		change_step(2, 3);
		current_step = 3;

}

function gotostep1()
{
	change_step(current_step, 1);
	current_step = 1;
}

function gotostep2()
{
	change_step(current_step, 2);
	current_step = 2;

}

function gotostep3()
{
	change_step(current_step, 3);
	current_step = 3;
}





function change_step(step_old, new_step)
{
	document.getElementById("step" + step_old).style.display ="none";
	document.getElementById("step" + new_step).style.display ="block";
}
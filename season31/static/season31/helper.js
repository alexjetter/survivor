function startTimer(duration) 
{
	var scriptTag = document.scripts[document.scripts.length - 1];
	var display = scriptTag.parentNode;
	var timer = parseInt(duration,10), days, hours, minutes, seconds;
	setInterval(function () 
	{
		days    = parseInt((timer             ) / (24*60*60), 10);
		hours   = parseInt((timer % (24*60*60)) / (   60*60), 10);
		minutes = parseInt((timer % (   60*60)) / (      60), 10);
		seconds = parseInt((timer % (      60))             , 10);

		if (days > 0)
			display.innerHTML = days + " day(s), " + hours + " hour(s), " + minutes + " minute(s) left";
		else if (hours > 0)
			display.innerHTML = hours + " hour(s), " + minutes + " minute(s) left";
		else
			display.innerHTML = minutes + " minute(s) left";

		if (--timer < 0) 
			timer = 0;
	}, 1000);
}

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
			if (days > 1)
				if (hours != 1)
					display.innerHTML = days + " days, " + hours + " hours";
				else
					display.innerHTML = days + " days, " + hours + " hour";
			else
				if (hours != 1)
					display.innerHTML = days + " day, " + hours + " hours";
				else
					display.innerHTML = days + " day, " + hours + " hour";
		else
			display.innerHTML = hours + ":" + minutes + ":" + seconds;

		if (--timer < 0) 
			timer = 0;
	}, 1000);
	// 7 days in seconds = 604800
}

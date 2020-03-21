
osascript -e "
	tell application \"System Events\"
		set frontmost of the first process whose unix id is $1 to true
	end tell
"

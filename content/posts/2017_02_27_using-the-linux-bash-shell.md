Title: Using the Linux bash shell
Date: 2017-02-27 20:13
Tags: Code
Category: Other
Slug:using-the-Linux-bash-shell

Man, it is been awhile. So the topic of bash shell scripting. Consider my problem:


I always download stuff to read later on. I am sort of a hoarder in that regard.(I hoard text files and pdfs). Anyways I have always used Nautils(Nautils is the GUI that gives the windows and that "Microsofty" look to Linux systems) to copy my downloaded files to the location I want them to go to. I desperately wanted to use the command line to automate that process. I recently contributed to a [zsh](http://www.zsh.org/) theme called [Geometry](https://github.com/frmendes/geometry/) which I use on my FreeBSD machine.(BTW, I think it is a fantastic beginner's project to contribute to, but I digress). 


So the problem stated more formally is:


> Automate the copying of recently downloaded files to user-defined directories. The user should have the option of specifing the number of files that they want to copy and if they want the copied file to have the same name as the original.


Whew!! That was a mouthful. Onto the task of coding up this badboy!!


Now what is the way this function would be called? I like the way `ls` operates. U can either call `ls -l`(ls long-format), `ls -r`(list in reverse format) and `ls -l -r`(ls long-format in reverse). These are called options. So this command, I am calling it **cpRecent** , should have options for the number of files and an edit option. Ideally we want this new function to behave similarly to `cp`. So the format could be 


> cpRecent -d {directories} -n {number of files} -i{interactive or edit mode} -h{help}


The last option *-h* is sort of mandatory as it makes the command in line with most of commands in linux and we want it that a new user can use the function upon reading the help menu, accessed through the *-h* option. Also a "sort of" standard is to put your user-defined functions in the `bash_aliases` file. Now, lets see the help menu(encapsulated by our `__usage()` function):


    __usage(){

    cat <<End-Of-Message
    _______________________________________________________________________________
    Copies/Moves the n most recent file(s) in a directory to another directory where
    n is user specified. 
    
    <cpRecent/mvRecent> [-d "D1,D2"] [-n NUM] [-ih]
    
	    -d "D1,D2"	The directory that is copied/moved from is D1 while  
			        the directory that is copied/moved to is D2 
			        The directories would need to be in relative paths
	    -n 		    This specifies an integer num of files 
	    -i		    This allows the user to edit the name of the file
		    	    to be copied or moved 	
	    -h		    Shows this entire wall of text 		
			
    An example of how to use the command:
	
	cpRecent -d "Documents,." -n 3
	
	(This means that copy the three(3) most recent files in Documents to 
	the folder I am currently in)
    _______________________________________________________________________________
    End-Of-Message
    }

  
The above is called a *here document*. It allows for self-documenting code and we can use it to store our help menu. Important caveats:


> The string on the last line must not have any spaces in front of it.
> 
> 
> Dont use `wall`. `Wall` sends the message to all the users logged into the system. Ideally you want the message to go to the current user executing the script.


If you noticed, the usage function has preceding double underscores. That is "sort of" a [convention](http://stackoverflow.com/questions/13797087/bash-why-double-underline-for-private-functions-why-for-bash-complet). How do we process these options **-d, -n, -i, -h**? We use a shell command called `getopts`. Another caveat: `getopts` only processes short options( just one dash infront of the character). Long options are more descriptive like *--number instead of -n* in our description. There is a way to do [that](http://mywiki.wooledge.org/BashFAQ/035) but I am too lazy.  We also are going to put all our option processing into another function.  


    __processoptions(){
	    OPTIND=1
	    while getopts ":d:n:ih" opt; do
		    case $opt in 
			    d ) IFS=',' read -r -a directories <<< "$OPTARG";; 
			    n ) numfiles=$OPTARG;;
			    i ) interactive=1;;
			    h ) __usage; return 1;;
			    \? ) echo "$invalid_option -$OPTARG" >&2 ; return 1;;
			    : ) echo "$no_args"; __usage >&2 ; return 1;;
			    * ) __usage >&2; return 1;;
		    esac
	    done	
	    shift "$((OPTIND-1))"
    
	    # Check for errors	
	    (( ${#directories[@]} != 2 )) && echo "$invalid_option Number of directories must be 2" && return 2
	
	    __returnfullpath "${directories[0]}"
	    directories[0]="$fullpath"
	    __returnfullpath "${directories[1]}"
	    directories[1]="$fullpath"	
    
	    if [[ -z ${directories[0]} || -z ${directories[1]} ]]; then
		    echo $no_directory 
		    return 3
	    fi
    
	    [[ numfiles != *[!0-9]* ]] && echo "$invalid_option Number of files cannot be a string" && return 4
    
	    (( $numfiles == 0 )) && echo "$invalid_option Number of files cannot be zero" && return 4
    
	    return 0
    } 


The `(( ))` indicate mathematical evaluation while `[[ ]]` is for `test`(conditional expressions). **A fun way to check all the conditional expressions that is there is to do this on your command line `man test`** .`>&2` is a way to print to `sterr` instead of `stout`. We use `return` instead of `exit` because we are going to put this code in `bash_aliases` file. An `exit` commad would cause our current shell to terminated prematurely. The line `IFS=',' read -r -a directories <<< "$OPTARG";; ` is to split the string from `OPTARG` into two substrings at any `,`. `IFS` is kinda of global and we do not want to set it so we put it on the same line as the `read` command . This part `read -r -a directories <<< "$OPTARG"` is just redirecting the string into an array called **directories**. 


So we get an invocation of the command like: `cpRecent -d "Downloads,." -n 2`. We need to check that the user has inputted directories that are on the system. (I mean, you can't copy from thin air into thin air). That is the function of the `__returnfullpath` function as shown below:


    # Advise that you use relative paths
    __returnfullpath(){
	    local npath
	    if [[ -d $1 ]]; then
		    cd "$(dirname $1)"
		    npath="$PWD/$(basename $1)"
		    npath="$npath/"			# Add a slash
		    npath="${npath%.*}"		# Delete . 
	    fi
	    fullpath=${npath:=""}
    } 


`local variable` basically makes `variable` to have *function-scope*, that is, `variable` only lives in a function. `dirname` basically gets the parent directory of our directory and `basename` returns a filename from a path.  


The other variables that we are going to be using is shown below:


    #Error codes
    no_args="You need to pass in an argument"
    invalid_option="Invaild option:"
    no_directory="No directory found"
    
    # Return values 
    fullpath=
    directories=
    numfiles=
    interactive=
    
    typeset -a files
    typeset -A filelist   


The `typeset` is a way to declare a variable as an array. `typeset -A` initialises an associative array, kinda like a dictionary and `typeset -a` initialises an normal array. 


Continuing with our eariler example, we have to get the 2 most recent files from the *Downloads* directory. We do that with another function:


    __getrecentfiles(){
	
	    local num="-"$numfiles""
	
	    # Get the requested files in directory(skips directories)
	    if [[ -n "$(ls -t ${directories[0]} | head $num)" ]]; then
		    # For some reason using local -a or declare -a does not seem to split the string into two
		    local tempfiles=($(ls -t ${directories[0]} | head $num))
		    for index in "${!tempfiles[@]}"; do
			    echo $index ${tempfiles[index]}
			    [[ -f "${directories[0]}${tempfiles[index]}" ]] && files+=("${tempfiles[index]}") 
		    done
	    fi
    
	    return 0
    } 


Basically, we make use of `ls -t`(ls with timestamps arranged from most recent to least recent) and `head` to get the list of files. Then we check if the files themselves are directories with the `-f` test. If they are, we add them to *files* array. Okay, we need to do one last thing, we need to get the full path of the files so that `cp` would not complain!!  We use the *__processlines* function to do that:


    __processlines(){
	    local name
	    local answer
	    if [[ -n $interactive ]]; then
		    for index in "${!files[@]}"; do
			    name=${files[index]}
			    read -n 1 -p "Old name: $name. Do you wish to change the name(y/n)?" answer
			    # Need to leave a space in between the variables 
			    [[ "$answer" == "y" ]] && read -p "Enter new name:" name
			    local dirFrom="${directories[0]}${files[i]}"
			    local dirTo="${directories[1]}$name"
			    filelist+=(["$dirFrom"]="$dirTo")
		    done
	    else									
		    for index in "${!files[@]}"; do
			    local dirFrom="${directories[0]}${files[index]}"
			    local dirTo="${directories[1]}${files[index]}"
			    filelist+=(["$dirFrom"]="$dirTo")
		    done	
	    fi
    
	    return 0
    } 


We check for the interactive option (*-i*). If the user specified interactive, we ask if they want to keep the names or change them using these lines:


> read -n 1 -p "Old name: $name. Do you wish to change the name(y/n)?" answer


This line prompts the user with the old name of the file and asks the user if he/she wants to change it. The `read`	command is a way to read user input and in this case, it only reads one character, either a "y" or a "n".`-n` means "number of characters" and `-p` is for prompt. The value is stored in answer:


> [[ "$answer" == "y" ]] && read -p "Enter new name:" name


This line checks if the answer is "y". If it is, it asks for the new name. We then associate the old name of the file with the new name of the file: `filelist+=(["$dirFrom"]="$dirTo")`.  Now I had run all this in one script file , but because I did not want to pollute my `bash_aliases` file, I decided to put all the above code into a helper library: *helperlib.sh*(Imaginative, huh?) So where do we use this helperlib.sh? We get to use it in the main function, **cpRecent**. Another reason for using the library was to see if I could also use the code to do a `mv`(move command) style command. Turns out I could. Okay, enough stalling. Here is the main `bash_aliases` file:


[gist:id=d2740d54db7c13cd88b0bb1cbb8f8198]


The first line in the **cpRecent** command is to *source* the helperlib.sh. If you have used Java with its `import` statement or C++ with its `include` statement, it bascially does the same thing. Another thing with `return` and `exit`,it normally returns the status of the last command. The status of the last command is in the variable `$?`. If the status is `0`, then we know that the command was successful. Any other number indicates a failure and that is what this `(( $? == 0 ))` is checking. `unset` is normally used with arrays to deference(delete) them. So the helperlib.sh is shown below:


[gist:id=5aff1a8f6b49d4402c46f23720e36295]


Okay, I learnt a lot of patience while coding up this solution. Also `bash -x` is a powerful way of looking at how your bash program executes, basically debugging. Use it liberally!!!!


**One caveats**:


> Presently the directories should be relative paths. I have not found a way to get the path of any file with using some third party library. 

To see it in action, 


![Bash program execution]({filename}../images/bash_command_output.gif)
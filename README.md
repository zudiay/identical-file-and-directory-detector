# identical-file-and-directory-detector
The program traverses the directories and look for files or directories that are duplicates of each other (i.e. identical). The full pathnames of duplicates will be printed as output.

The program can be invoked with the following options and arguments:<br>
```identic [-f | -d ] [-c] [-n] [-s] [<dir1> < dir2> ..]```

<br>```[-f | -d ]``` -f	means	look	for	identical files,	-d	means	look	for	identical
directories.	The	default	is	identical files.	
<br>```-c``` Identical will	mean	the	contents	are	exactly	the	same	(note	
that	the	names	can	be	different).
<br>```-n``` Identical		will	mean	the	directory/file	names are	exactly	the	
same	(note	that	the	contents can	be	different).
<br>```-cn``` Identical	 will	mean	both	the	contents	and	the	directory/file	
names	are	exactly	the	same.
<br>```[<dir1> <dir2> ..]``` The	list	of	directories	to	traverse	(note	that	the	directories	
will	be	traversed	recursively,	 i.e.	directories	and	their	
subdirectories	and	their	subdirectories	etc.	etc.).	 The	
default is	current	directory.	
<br>```-s``` The	size		for	each	duplicate will	also	be		printed.	The	
duplicates	should	be	printed	in	descending	order	of	size.
This	option	is ignored	when	–n	option	is	used.	


It is assumed	that	directory	hierarchy	forms	a	tree. It is assumed	there	are	no	symbolic	links.	<br>
• The program uses sha256	hashes	in	order	to	locate	identical	items.	<br>
• To	locate	identical directories,	hash	trees are used.<br>


<i> Developed for CMPE 230 SYSTEMS PROGRAMMING course, Bogazici University Computer Engineering, Spring 2020. <i>

Dependency installation
===

Run the installers in the following order:
* install_winget 
	* this is manual; you need to download .msixbundle
	
* install_7z 
	* If you've already got 7zip installed, you may need to add it to PATH
	* If it's not installed, this process will install it for you.

* install_ffmpeg
	* If you've already got ffmpeg on the PATH, this will be skipped
	* Otherwise we will download a copy, un-7zip it and then add that to PATH

* install_python
	* If you've already got `python` on the PATH, this will be skipped.
	
* add_discordvid_to_path
	* If you've already got `dv.bat` on the PATH, this will be skipped.


What is `PATH`?
===
`PATH` is a variable that allows you to run programs from 
command line more easily. You can run programs without
having to know which directory they came from.

Adding various folders to the `PATH` is crucial for the
operation of this program.
Before starting the EVIS web server:
  1. Python must be install and all the modules the EVIRS python code requires.
     The Path variable must have been set in the Environment Variable System Properties window
     The Path variable should include these two paths
       C:\Program Files\Python\Python39\Scripts\
       C:\Program Files\Python\Python39\

  2. Required python modules
     python -m pip install tornado
     python -m pip install numpy
     python -m pip install pandas
     python -m pip install vininfo

  3. You may want to check the port setting.
     When code is moved here, it usually is set to start the web server on port 8882.
     To change the port to the normal port 80, open index.py and look for the line that
     reads "port = xxxx" (where xxxx may be 8882). Change that to read "port = 80"

To start the EVIS web server:
  1. Open a CMD prompt 
        Click on the Windows icon in the lower left corner, then type: cmd (and press enter)
  2. In the CMD window, navigate to C:\EVIRSWEB. 
        Type: C:\EVIRSWEB (and press enter)
  3. In the CMD window, start python and run index.py. 
        Type: python index.py (and press enter)

Test on this server by opening a Chrome or Edge and navigate to:
   http://evirsapptst.inl.gov (for port 80)
   http://evirsapptst.inl.gov:8882 (for port 8882 in this example)
  If this fails, perhaps python or the index.py didn't start

Test on your local computer by navigating to the same URL.
  If this fails, and the web page run OK on the server, perhaps you don't have permission to access the EVIRSAPPTST server.

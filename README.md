# COntaminant behavior in Air, Liquids, and Solids (COALS) Controls Tool

The *CO*ntaminant behavior in *A*ir, *L*iquids, and *S*olids (COALS) Controls Tool is a model to predict the behavior of several trace elements in coal-fired power plants.  These trace elements include:
<ul>
  <li> Arsenic </li>
  <li> Boron </li>
  <li> Bromine </li>
  <li> Chlorine </li>
  <li> Lead </li>
  <li> Mercury </li>
  <li> Selenium </li>
  </ul>
A user can specify the rank of coal combusted, the amount of electricity generated, and installed air pollution and water pollution control devices.  The model then returns the amount of trace elements that leave the coal-fired power plant in the gas (i.e., exhaust gas), solid (i.e., bottom ash, fly ash, and gypsum), and liquid (i.e., FGD wastewater).  The model also additionally reports the estimated concentration of FGD wastweater and whether the water pollution treatment technologies htat are installed will be sufficient to achieve compliance with the Effluent Limitation Guidelines and Standards.

For more information on the tool (including a list of the papers underlying the trace element partitioning behavior models) and how to use the GUI, please see the <a href="https://osf.io/6rfe8/"> Open Science Foundation project </a>.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Creating an instance of the GUI using Python
To create the GUI using Python (rather than by installing the GUI), run the trace_element_GUI.py file located in the Code/GUI directory.

### Installing the GUI 
To install the COALS Controls GUI download the COALS Controls Model.msi file.  After the download completes, double click to run the file.  The installer will start.  You will need to select a location and the file will then install the executable.

This GUI is currently only for Windows machines.  An Apple version is currently in development.

## Contributing

Please read CONTRIBUTING.md for details of our code of conduct, and the process for submitting pull requests to us.

### Reporting a Bug
To report a bug, create an issue in the GitHub Repository.  Please use the <a href="https://github.com/we3lab/coals_controls/issues/new?assignees=&labels=&template=bug_report.md&title="> Bug Report template </a>.

### Requesting a Feature
To requiest a feature, create an issue in the GitHub Repository.  Please use the <a href="https://github.com/we3lab/coals_controls/issues/new?assignees=&labels=&template=feature_request.md&title="> Feature Request template </a>.

## Authors
<ul> 
  <li> Jiachen Liu, Carnegie Mellon University, jiachen6@andrew.cmu.edu </li>
  <li> Daniel Gingerich, Stanford University, dbginger@stanford.edu </li>
  </ul>
  
## License

This project is licensed under the MIT License - see the <a href="https://github.com/we3lab/coals_controls/blob/master/LICENSE"> LICENSE.md </a> file for details.

## Acknowledgements
The development of the tool was supervised and fudnign was secured by Professor Meagan S. Mauter.  The COALS Controls Tool is based on modelling work initially done in a project with Xiaodi Sun and Ines Azevedo. 

In adition, we would like to thank the following funding sources:  
<ul>
  <li> U.S. Department of Energy and the National Energy Technology Laboratory under contract DE-FE0031646 </li>
  <li> U.S. Department of Energy Oak Ridge Institue for Science Education program </li>
  <li> U.S. National Science Foundation under contract CBET-1554117 </li>
    

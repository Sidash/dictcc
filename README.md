# dictcc
Simple python command line client for dict.cc.


Usage:

search in both directions:
> dictcc.py <dictfrom><dictto> <search>

or for one directional search:
> dictcc.py <dictfrom>-<dictto> <search>


Possible dictionaries <dict> are
Primary: en de
Secondary: fr sv bs cs da el bg eo es fi hr hu is it la nl no pl pt ro ru sk sq sr tr
Examples
> ./dictcc.py enfr  <search> (search in two directions)
> ./dictcc.py de-fr <search> (sarch from de to fr)
> ./dictcc.py fr-en <search>
> ./dictcc.py ende  <search>

for a comprehensive list see http://dict.cc/

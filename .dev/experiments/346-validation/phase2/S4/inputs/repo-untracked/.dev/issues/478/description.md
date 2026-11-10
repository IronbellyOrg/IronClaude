# Description given to /sc:issue --create

Title: BMAD and Ponytail not accessible globally by default

BMAD and Ponytail are only accessible on projects where the user has previously installed them. They are not installed by default on all projects and are not available globally to the user. BMAD, if accessed on a project where it has never been used or installed, should create the necessary directories on that project to function, if they do not exist already.

Context given by the coordinator: repository IronbellyOrg/Coder; the area is how the AIDev02 template image and catalogue install and expose BMAD and Ponytail (templates/VSCode-AIDev02/image/ including catalogue/, aienv.d/ and the image Dockerfile, and docs). Do not assume where BMAD or Ponytail come from; establish it from code.

FROM google/cloud-sdk:latest

RUN apt-get update && apt-get upgrade
RUN apt-get install nano 

CMD ["/bin/bash"]


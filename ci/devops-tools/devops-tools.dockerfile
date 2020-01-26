FROM google/cloud-sdk:latest

RUN hwclock --hctosys
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y nano 

CMD ["/bin/bash"]


####################################################################################################
#
# Shell functions
#
####################################################################################################

append_to_python_path_if_not ()
{
  for i in $*;
  do
    if [ -z ${PYTHONPATH} ]; then
      PYTHONPATH=$i;
    else
      ! $(${path_tools} -s $i ${PYTHONPATH}) && PYTHONPATH=$i:${PYTHONPATH};
    fi;
  done;
  export PYTHONPATH
}

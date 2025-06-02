user_count=$(oc get namespaces | grep showroom | wc -l)

WORKBENCH_NAME="my-workbench"

for i in $(seq 1 $user_count);
do

# Construct dynamic variables
USER_NAME="user$i"
USER_PROJECT="user$i"

if [ -z "$(oc get pods -n $USER_PROJECT -l app=$WORKBENCH_NAME -o custom-columns=STATUS:.status.phase --no-headers | grep Running)" ]; then
    echo "$USER_PROJECT workbench is not running."
fi

done
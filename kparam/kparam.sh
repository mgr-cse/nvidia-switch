#!/bin/bash

grub_file="./grub"
key="GRUB_CMDLINE_LINUX_DEFAULT"

if [ ! -f $grub_file ]; then
    echo "can\'t open grub file, exiting..."
    exit 2
fi

# search parameters in file
search="^$key=\"(.*)\""
params=`sed -nE "s/$search/\1/p" $grub_file`

# extract parameters as array
params=($params)

param=""

usage () {
    echo "This utility manages kernel parameters in /etc/default/grub
usage: $0 [flags] [kernel-parameter]
    flags:
        -s          show current kernel parameters
        -d PARAM    delete PARAM from parameter list
        -a PARAM    add param to parameter list
        -h          print this message"

}

write () {
    param_str="\"${params[@]}\""
    sed -Ei "s/$search/$key=$param_str/" $grub_file
}

add () {
    flag="0"
    for x in "${params[@]}"; do
        if [ "$x" = "$param" ]; then
            flag="1"
            break
        fi
    done

    if [ "$flag" = "0" ]; then
        params+=("$param")
    fi

    write
    #update-grub
}

delete () {
    for i in "${!params[@]}"; do
        [ "${params[i]}" = "$param" ] && unset 'params[i]'
    done

    for i in "${!params[@]}"; do
        new_params+=("${params[i]}")
    done
    parameters=("${new_params[@]}")
    unset new_params

    write
    #update-grub
}

show () {
    echo "${params[@]}"
}

# parsing
while getopts "a:d:sh" arg; do
    option="true"
    case $arg in
        s)
            show_params="true"
            ;;
        a)
            param=$OPTARG
            add
            ;;
        d)
            param=$OPTARG
            delete
            ;;
        *|h)
            usage
            ;;
    esac
done

[ ! "$option" = "true" ] && usage
[ "$show_params" = "true" ] && show
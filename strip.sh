#!/bin/bash

EXECUTABLES=$(find -maxdepth 1 -name '*.dll')" "$(find -maxdepth 1 -name '*.exe')" "$(find AI/Skirmish -name SkirmishAI.dll)" "$(find AI/Interfaces -name AIInterface.dll)" "$(find -name pr-downloader_shared.dll)
DEBUGFILES=""

for tostripfile in ${EXECUTABLES}; do
  if [ -f ${tostripfile} ]; then
    if ! objdump -h ${tostripfile} | grep -q .gnu_debuglink; then
            echo "stripping ${tostripfile}"
            debugfile=${tostripfile%.*}.dbg
            (objcopy --only-keep-debug ${tostripfile} ${debugfile} && \
            strip --strip-debug --strip-unneeded ${tostripfile} && \
            objcopy --add-gnu-debuglink=${debugfile} ${tostripfile}) &
            DEBUGFILES="${DEBUGFILES} ${debugfile}"
        else
            echo "not stripping ${tostripfile}"
        fi
    fi
done

wait

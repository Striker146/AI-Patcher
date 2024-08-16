cd ros-humble
call micromamba run -n devenv boa build recipes -m ./.ci_support/conda_forge_pinnings.yaml -m ./conda_build_config.yaml > ../boa_log.txt
COMMON=-O2 -I${MUJOCO_PATH}include -L${MUJOCO_PATH}bin -std=c++11 -mavx -pthread -Wl,-rpath,'$$ORIGIN'

all:
	g++ $(COMMON) main.cpp -lmujoco200 -lGL -lglew ${MUJOCO_PATH}bin/libglfw.so.3 -o bin/main
	# gcc -c -O2 -mavx -I${MUJOCO_PATH}include ${MUJOCO_PATH}include/uitools.c
	# g++ $(COMMON) uitools.o simulate.cpp -lmujoco200 -lGL -lglew ${MUJOCO_PATH}bin/libglfw.so.3 -o bin/simulate
	# rm *.o
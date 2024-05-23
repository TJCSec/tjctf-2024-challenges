.PHONY: all clean solve

CPPFLAGS=-std=c++20 -static-libstdc++ -static-libgcc

LIB = sphere_engine.cpp common.cpp updater.cpp

SRCS = main.cpp $(LIB)

SOLVE_SRCS = solve.cpp $(LIB)

OBJS = $(subst .cpp,.o,$(SRCS))

SOLVE_OBJS = $(subst .cpp,.o,$(SOLVE_SRCS))

all: outp

outp: $(OBJS)
	g++ $(CPPFLAGS) -o ../out $(OBJS)
	
%.o: %.cpp
	g++ $(CPPFLAGS) -c $<

solve: slv

slv: $(SOLVE_OBJS)
	g++ $(CPPFLAGS) -o ../solve $(SOLVE_OBJS)

clean:
	rm -rf *.o
	rm -rf out solve

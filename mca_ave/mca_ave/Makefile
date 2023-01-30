PROGRAM = bnd
OBJS = mca_ave.o create_cdf.o gattr.o vattr.o
SRCS = mca_ave.c create_cdf.c gattr.c vattr.c
HEADER = average.h

$(PROGRAM):	$(OBJS)
	gcc -o $(PROGRAM) $(OBJS) -lcdf -lm -lc
$(OBJS):        $(HEADER)
.c.o:
	gcc -c $<
clean:
	rm $(OBJS) $(PROGRAM)

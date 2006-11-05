CSC = gmcs

SRC = $(wildcard *.cs)
OBJ = $(subst cs,dll,$(SRC))

all: $(OBJ)

clean:
	rm -f $(OBJ)

WSGI.dll: WSGI.cs
	$(CSC) -t:library -r:System.Web.dll -r:System.Configuration.dll -r:IronPython.dll $<


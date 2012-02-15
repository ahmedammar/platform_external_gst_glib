## Process this file with automake to produce Makefile.in
include $(top_srcdir)/Makefile.decl

INCLUDES = $(glib_INCLUDES) -DG_LOG_DOMAIN=\"GLib\" \
	$(GLIB_DEBUG_FLAGS) -DG_DISABLE_DEPRECATED -DGLIB_COMPILATION 

noinst_LTLIBRARIES = libgnulib.la

libgnulib_la_SOURCES = 	\
	asnprintf.c \
	printf-args.c \
	printf-args.h \
	printf-parse.c \
	printf-parse.h \
	vasnprintf.c \
	vasnprintf.h \
	printf.c \
	printf.h \
	g-gnulib.h

Android.mk: Makefile.am
	androgenizer -:PROJECT glib -:STATIC libgnulib -:TAGS user eng debug \
	 -:REL_TOP $(top_srcdir) -:ABS_TOP $(abs_top_srcdir) \
	 -:SOURCES $(libgnulib_la_SOURCES) \
	 -:CFLAGS $(DEF) $(CFLAGS) $(INCLUDES) \
	> $@

EXTRA_DIST += makefile.msc

# This file is the top android makefile for all sub-modules.

LOCAL_PATH := $(call my-dir)

glib_TOP := $(LOCAL_PATH)

include $(CLEAR_VARS)

glib_TOP := $(LOCAL_PATH)

glib-configure-real:
	cd $(glib_TOP) ; \
	CC="$(CONFIGURE_CC)" \
	CFLAGS="$(CONFIGURE_CFLAGS)" \
	LD=$(TARGET_LD) \
	LDFLAGS="$(CONFIGURE_LDFLAGS)" \
	CPP=$(CONFIGURE_CPP) \
	CPPFLAGS="$(CONFIGURE_CPPFLAGS)" \
	PKG_CONFIG_LIBDIR="$(CONFIGURE_PKG_CONFIG_PATH)" \
	PKG_CONFIG_TOP_BUILD_DIR=/ \
	ac_cv_header_pwd_h=no \
	ac_cv_header_locale_h=no \
	glib_cv_langinfo_codeset=no \
	$(abspath $(glib_TOP))/$(CONFIGURE) \
	--host=arm-linux-androideabi \
	--prefix=/system \
	--enable-included-printf=yes \
	--with-libiconv=no \
	--enable-iconv-cache=no \
	--disable-regex && \
	for file in $(GLIB_BUILT_SOURCES); do \
		rm -f $$file && \
		make -C $$(dirname $$file) $$(basename $$file) ; \
	done

GLIB_BUILT_SOURCES := \
	gio-2.0-uninstalled.pc \
	gio-2.0.pc \
	gio-unix-2.0-uninstalled.pc \
	gio-unix-2.0.pc \
	gio-windows-2.0.pc \
	glib-2.0-uninstalled.pc \
	glib-2.0.pc \
	gmodule-2.0-uninstalled.pc \
	gmodule-2.0.pc \
	gmodule-export-2.0.pc \
	gmodule-no-export-2.0-uninstalled.pc \
	gmodule-no-export-2.0.pc \
	gobject-2.0-uninstalled.pc \
	gobject-2.0.pc \
	gthread-2.0-uninstalled.pc \
	gthread-2.0.pc \
	gio/Android.mk \
	glib/gnulib/Android.mk \
	glib/libcharset/Android.mk \
	glib/Android.mk \
	gmodule/Android.mk \
	gobject/Android.mk \
	gthread/Android.mk

GLIB_BUILT_SOURCES := $(patsubst %, $(abspath $(glib_TOP))/%, $(GLIB_BUILT_SOURCES))

glib-configure: glib-configure-real

.PHONY: glib-configure glib-configure-real
CONFIGURE_TARGETS += glib-configure

-include $(glib_TOP)/glib/Android.mk
-include $(glib_TOP)/gmodule/Android.mk
-include $(glib_TOP)/gthread/Android.mk
-include $(glib_TOP)/gobject/Android.mk
-include $(glib_TOP)/gio/Android.mk


# Unfortunately, we can't really build executables with the NDK, can we? FIXME:
# write a java program that runs the test through some JNI magic
# include $(glib_TOP)/tests/Android.mk


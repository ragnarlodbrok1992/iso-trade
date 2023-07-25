// Basic top level imports
#import "Basic";
#import "GL";
#import "Window_Creation";
#import "Input";

// Named imports
Simp :: #import "Simp";
GetRect :: #import "GetRect";

// Version of engine - 0.0.0 before pre-alpha
MAJOR_VERSION := 0;
MINOR_VERSION := 0;
BABY_VERSION := 0;

// Engine consts
// @TODO: create this string in compile time with engine version number
WINDOW_TITLE_BAR : string = "Iso Trade - developer version: %.%.%";

// Engine variables
// @TODO: Check this code on MacOS - when Jai is ready
ENGINE_SHOULD_QUIT := false;
#if OS == .LINUX {
  MAIN_ENGINE_WINDOW : u64;
} else {
  MAIN_ENGINE_WINDOW : *void;
}

main :: () {
  // Start information
  print("Iso Trade! Starting up engine.\n");
  print("Version: %.%.%\n", MAJOR_VERSION, MINOR_VERSION, BABY_VERSION);
  defer print("Iso Trade successfully ended!\n");

}

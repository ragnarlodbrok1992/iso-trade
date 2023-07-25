#run build();

build :: () {
  // Creating workspace
  w := compiler_create_workspace("Target Program");

  // Getting build options
  options := get_build_options();
  options.output_executable_name = "iso-trade";
  set_optimization(*options, .DEBUG);
  set_build_options(options, w);

  // Begin intercepting messages @TODO - for now we don't do
  // much of a metaprogramming

  // Begin intercepting messages

  // Adding code @DONE - should this be done? YES
  // @TODO - should every file be added here?
  add_build_file(tprint("%/src/iso_trade.jai", #filepath), w);

  // Looping over compiler messages

  // End compiler intercepting

  // Do not emit code for this program
  set_build_options_dc(.{do_output = false});
}

#import "Basic";
#import "Compiler";


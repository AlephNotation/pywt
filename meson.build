project(
  'PyWavelets',
  'c', 'cython',
  version: '1.10.0.dev0',
  license: 'MIT',
  meson_version: '>= 1.11.0',
  default_options: [
    'buildtype=debugoptimized',
    'b_ndebug=if-release',
    'c_std=c17',
  ],
)

py = import('python').find_installation(pure: false)
cc = meson.get_compiler('c')
m_dep = cc.find_library('m', required: false)
if m_dep.found()
  add_project_link_arguments('-lm', language: 'c')
endif

use_rust = get_option('use-rust')
pywt_rust = []
if use_rust
  add_languages('rust', native: false)
  # Meson's Cargo interpreter does not consume Cargo profile settings. Preserve
  # the release profile's cross-crate thin LTO explicitly for the Rust archive.
  rust_global_args = ['-Cembed-bitcode=yes']
  if host_machine.cpu_family() == 'x86_64'
    # SSE4.2 adds a third copy of the SIMD kernels without widening the x86-64
    # baseline. Dispatch directly from the baseline to AVX2 or AVX-512.
    rust_global_args += ['--cfg', 'disable_dispatch_sse4_2']
  endif
  add_global_arguments(rust_global_args, language: 'rust')
  rustmod = import('rust')
  cargo_workspace = rustmod.workspace()
  pywt_rust = cargo_workspace.package().library(
    install: false,
    rust_args: ['-Clto=thin'],
  )
endif

cython = find_program('cython')

py_dep = py.dependency()

subdir('pywt')

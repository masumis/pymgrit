# ./masumi_test_diffusiononly.sh 2>&1 > masumi_test_diffusiononly.out &

########
# Test diffusion with that driver, 1.0 vs. 1.3

# Order 1 tests
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.0 -nt 128 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.3 -nt 128 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.6 -nt 128 
#
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.0 -nt 512 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.3 -nt 512 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.6 -nt 512 
#
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.0 -nt 2048 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.3 -nt 2048
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.6 -nt 2048
#
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.0 -nt 8192
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.3 -nt 8192
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -1   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.6 -nt 8192


# Order 2 tests
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.0 -nt 256 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.3 -nt 256 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.6 -nt 256 
#                                                                                                                      
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.0 -nt 512 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.3 -nt 512 
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.6 -nt 512 
#                                                                                                                      
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.0 -nt 1024
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.3 -nt 1024
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.6 -nt 1024
#                                                                                                                      
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.0 -nt 2048
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.3 -nt 2048
mpirun -np 16 ./drive-diffusion -fe 1 -odesolver -2   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.6 -nt 2048


# Order 3 tests
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.0 -nt 256 
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.3 -nt 256 
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 1 -CWt 1.6 -nt 256 
#                                                                                                                      
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.0 -nt 512 
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.3 -nt 512 
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 2 -CWt 1.6 -nt 512 
#                                                                                                                      
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.0 -nt 1024 
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.3 -nt 1024
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 3 -CWt 1.6 -nt 1024
#                                                                                                                      
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.0 -nt 2048
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.3 -nt 2048
mpirun -np 16 ./drive-diffusion -fe 2 -odesolver -3   -access 0 -mi 75 -cf 2 -px 1 -tstop 15.0 -sref 4 -CWt 1.6 -nt 2048


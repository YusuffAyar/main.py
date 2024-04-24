from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_proc = comm.Get_size()
    number = 223908451
    sndnum = 0
    newnum = 0
    if rank == 0:
        start = MPI.Wtime()
        for i in range(1, 10):
            sndnum = number % 10
            comm.send(sndnum, dest=1, tag=99)
            number = number // 10
        number = -1
        comm.send(number, dest=1, tag=99)
    else:
        num = 9
        while True:
            newnum = comm.recv(source=rank-1, tag=99)
            if newnum < 0:
                break
            if rank < num_proc-1:
                if num < newnum:
                    comm.send(newnum, dest=rank + 1, tag=99)
                else:
                    comm.send(num, dest=rank + 1, tag=99)
                    num = newnum
            if number < newnum:
                number = newnum
        print(f"Thr-{rank}: {num}")
        if rank < num_proc - 1:
            num = -1
            comm.send(num, dest=rank + 1, tag=99)

if __name__ == "__main__":
    main()
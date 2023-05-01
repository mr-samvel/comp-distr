import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.ArrayList;

public interface ICinema extends Remote {
    public Boolean reservar(Integer cadeira) throws RemoteException;
    public ArrayList<Boolean> consultar() throws RemoteException;
}

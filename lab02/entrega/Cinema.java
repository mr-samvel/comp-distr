import java.lang.reflect.Array;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReferenceArray;

public class Cinema extends UnicastRemoteObject implements ICinema {
    private static final Integer MAX_CADEIRAS = 90;
    private AtomicReferenceArray<Boolean> cadeiras;
    
    protected Cinema() throws RemoteException {
        cadeiras = new AtomicReferenceArray<>(MAX_CADEIRAS);
        for (int i = 0; i < MAX_CADEIRAS; i++)
            cadeiras.set(i, true);
    }

    @Override
    public Boolean reservar(Integer cadeira) throws RemoteException {
        cadeira--;
        if (cadeira < 0 || cadeira >= MAX_CADEIRAS) return false;
        else if (cadeiras.get(cadeira)) {
            cadeiras.set(cadeira, false);
            return true;
        }
        return false;
    }

    @Override
    public ArrayList<Boolean> consultar() throws RemoteException {
        ArrayList<Boolean> arrCadeiras = new ArrayList<>();
        for (int i = 0; i < MAX_CADEIRAS; i++) {
            arrCadeiras.add(cadeiras.get(i));
        }
        return arrCadeiras;
    }
    
}

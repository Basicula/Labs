import parcs.*;

public class Map implements AM{
    public void run(AMInfo info){
        int x,y,r;
        x = info.parent.readInt();
        y = info.parent.readInt();
        System.out.println(x + '+' + y);
        r = x+y;
        info.parent.write(r);
    }
}

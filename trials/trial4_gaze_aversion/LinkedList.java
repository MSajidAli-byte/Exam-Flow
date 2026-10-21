public class LinkedList {
    Node head;
    static class Node{

        int data;
        Node next;
        Node(int d){data = d; next = null;}
    }
    public void insert(int data){
        Node newNode = new Node(data);

        if(head ==null){
            head = newNode;
        }else{
            Node temp = head;
            while(temp.next !=null){
                temp = temp.next;
            }temp.next = newNode;
        }
        
    }

    public void deleteNode(int key){
        Node temp = head, prev = null;

        // if head itself holds the key
        if(temp!=null && temp.data ==key){
            head = temp.next; //changing the head
            return;
        }
        // searching for the key to be deleted
        while(temp != null&& temp.data !=key){
            prev = temp;
            temp = temp.next;

        }
        // if key was not present
        if(temp == null) return;

        // unlike the node from the linked list
        prev.next = temp.next;
    }

    public void printList(){
        Node temp = head;
        while(temp != null){
            System.out.print(temp.data + " ");
            temp = temp.next;
        }
        System.out.println();
    }

    public static void main(String[] args){
        LinkedList list = new LinkedList();
        list.insert(10);
        list.insert(20);
        list.insert(30);
        list.insert(40);
        System.out.println("LinkedList");
        list.printList();

        list.deleteNode(20);
        System.out.println("After deletion of the key 20");
        list.printList();
    }
}

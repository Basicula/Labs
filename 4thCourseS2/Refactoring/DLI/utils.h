#include <string>
#include <vector>
#include <memory>
#include <ostream>


class Node 
  {
  public:
    using NodeSPtr = std::shared_ptr<Node>;
    
    Node() = default;
    Node(NodeSPtr i_node)
      : m_children(1)
      {
      m_children.push_back(i_node);
      }
    
    virtual ~Node() = default;
    
    void AddChild(NodeSPtr i_child)
      {
      m_children.push_back(i_child);
      }

    virtual void Print(const std::string& i_prefix, std::ostream& io_stream) const = 0;
  protected:
    std::vector<NodeSPtr> m_children;
  };

class Args : public Node 
  {
  public:
    Args(NodeSPtr i_arg)
      : Node(i_arg)
      {}
    
    void Append(NodeSPtr i_arg)
      {
      m_children.push_back(i_arg);
      }
    
    void Print(const std::string& i_prefix, std::ostream& io_stream) const override
      {
      io_stream << i_prefix << "ARGS(";
      for (const auto& child : m_children)
        child->Print(i_prefix + "    ", io_stream);
      io_stream << "    )"<<std::endl;
      }
  };
  
class Value : public Node
  {
  public:
    Value(const std::string& i_value)
      : Node()
      , m_value(i_value)
      {}
    
    void Print(const std::string& i_prefix, std::ostream& io_stream) const override
      {
      io_stream << i_prefix << m_value<<std::endl;
      }
  private:
    std::string m_value;
  };

typedef struct {
  std::string str;
  std::shared_ptr<Args> args;
  std::shared_ptr<Value> value;
  std::shared_ptr<Node> node;
} YYSTYPE;
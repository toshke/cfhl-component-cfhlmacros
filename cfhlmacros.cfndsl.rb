CloudFormation do

  CloudFormation_Macro('SubnetsMacro') do
    FunctionName Ref('cfhlmacros')
    Name 'CfHighlander_Networking'
  end

end